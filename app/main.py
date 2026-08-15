import json
import os
from fastapi import FastAPI, Request, Header, HTTPException, BackgroundTasks
from github import Github
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage

# Import your custom modules
from app.agent.github_client import post_pr_comment, get_raw_file_content, update_file_in_pr
from app.agent.graph import agent_app

load_dotenv()
app = FastAPI()
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")

def verify_github_signature(payload: bytes, signature: str, secret: str) -> bool:
    import hmac
    import hashlib
    if not signature or not secret:
        return False
    expected_signature = "sha256=" + hmac.new(
        secret.encode(), payload, hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected_signature, signature)

def run_agentic_pipeline(repo_full_name: str, pr_number: int, branch_name: str, changed_file_path: str):
    """This runs in the background so GitHub doesn't time out waiting for the AI."""
    print(f"🚀 Starting background AI pipeline for {changed_file_path}...")
    
    # 1. Fetch the RAW executable code
    raw_code = get_raw_file_content(repo_full_name, branch_name, changed_file_path)
    if not raw_code:
        print("Could not fetch raw code.")
        return
    
    # 2. Inject into LangGraph
    prompt = f"""
    Here is a raw Python file downloaded directly from a Pull Request:
    
    ```python
    {raw_code}
    ```
    
    Write a complete testable version of this code. Append test cases at the bottom (using `if __name__ == '__main__':`) 
    that aggressively execute the logic to find bugs. 
    Return ONLY valid, executable Python code so it can be executed in our Docker sandbox immediately.
    """
    
    initial_state = {
        "messages": [HumanMessage(content=prompt)],
        "iterations": 0
    }
    
    # 3. Run the LangGraph self-healing loop
    result = agent_app.invoke(initial_state)
    
    final_code = result.get("current_code")
    sandbox_result = result.get("sandbox_result", {})
    
    # 4. Push updates to GitHub
    if sandbox_result.get("success"):
        update_file_in_pr(
            repo_full_name=repo_full_name,
            branch_name=branch_name,
            file_path=changed_file_path,
            new_content=final_code,
            commit_message="🤖 fix: agentic-git autonomous repair"
        )
        final_comment = (
            f"🤖 **AgenticGit Autonomous Repair Complete**\n\n"
            f"The AI successfully tested and fixed the code in `{changed_file_path}` inside the Docker sandbox. "
            f"The fix has been automatically pushed to this branch.\n\n"
            f"### Sandbox Output:\n```\n{sandbox_result.get('output')}\n```"
        )
    else:
        final_comment = (
            f"🤖 **AgenticGit Repair Failed**\n\n"
            f"The AI attempted to fix the code but could not resolve the errors after {result.get('iterations')} iterations.\n\n"
            f"### Last Sandbox Crash Log:\n```\n{sandbox_result.get('output')}\n```"
        )
        
    post_pr_comment(repo_full_name, pr_number, final_comment)
    print("✅ Background pipeline finished!")

@app.post("/webhook/github")
async def github_webhook(request: Request, background_tasks: BackgroundTasks, x_hub_signature_256: str = Header(None)):
    payload = await request.body()
    
    if not verify_github_signature(payload, x_hub_signature_256, WEBHOOK_SECRET):
        raise HTTPException(status_code=401, detail="Invalid GitHub signature")
        
    event = json.loads(payload)
    action = event.get("action")
    if action not in ["opened", "synchronize"]:
        return {"status": "ignored", "reason": "Not a PR open or sync event"}
        
    pr_data = event.get("pull_request", {})
    pr_number = pr_data.get("number")
    repo_full_name = event.get("repository", {}).get("full_name")
    branch_name = pr_data.get("head", {}).get("ref")
    
    g = Github(os.getenv("GITHUB_TOKEN"))
    repo = g.get_repo(repo_full_name)
    pr = repo.get_pull(pr_number)
    
    # ==========================================
    # 🛑 NEW ANTI-LOOP CHECK
    # Get the latest commit on this PR
    commits = pr.get_commits()
    latest_commit = commits[commits.totalCount - 1]
    
    # If the bot made this commit, ignore the webhook!
    if "🤖 fix: agentic-git autonomous repair" in latest_commit.commit.message:
        print("Ignoring webhook: This commit was made by the bot.")
        return {"status": "ignored", "reason": "Bot's own commit"}
    # ==========================================
    
    changed_file_path = None
    for file in pr.get_files():
        if file.filename.endswith(".py"):
            changed_file_path = file.filename
            break
            
    if not changed_file_path:
        return {"status": "ignored", "reason": "No Python files changed"}

    # Hand the heavy work off to the background task!
    background_tasks.add_task(
        run_agentic_pipeline, 
        repo_full_name, 
        pr_number, 
        branch_name, 
        changed_file_path
    )

    # Immediately return a 202 Accepted so GitHub doesn't time out
    return {"status": "accepted", "message": "Agentic pipeline started in background"}