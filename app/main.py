from fastapi import FastAPI, Request, Header, HTTPException
import hmac
import hashlib
import json
import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from app.agent.graph import agent_app
from app.agent.github_client import post_pr_comment

load_dotenv()

app = FastAPI(title="AgenticGit Engine")

# This is a secret key we will set up in GitHub later to secure the connection
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "my-super-secret-key")

def verify_github_signature(payload: bytes, signature: str, secret: str) -> bool:
    """Verifies the webhook signature using HMAC and SHA-256."""
    if not signature or not signature.startswith('sha256='):
        return False
    expected = 'sha256=' + hmac.new(
        secret.encode(), payload, hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected, signature)

@app.post("/webhook/github")
async def github_webhook(request: Request, x_hub_signature_256: str = Header(None)):
    """
    Listens for GitHub Pull Request events.
    """
    # 1. Read the raw bytes FIRST to verify the signature
    payload = await request.body()
    
    # 2. Verify security
    if not verify_github_signature(payload, x_hub_signature_256, WEBHOOK_SECRET):
        raise HTTPException(status_code=401, detail="Invalid GitHub signature")
        
    # 3. Parse the JSON
    event = json.loads(payload)
    
    # We only care when a Pull Request is opened or updated
    action = event.get("action")
    if action not in ["opened", "synchronize"]:
        return {"status": "ignored", "reason": "Not a PR open or sync event"}
        
    # Extract PR details
    pr_data = event.get("pull_request", {})
    pr_number = pr_data.get("number")
    repo_full_name = event.get("repository", {}).get("full_name")
    pr_diff_url = pr_data.get("diff_url")
    
    # Formulate a prompt for the AI based on the PR diff
    prompt = f"Review the following GitHub Pull Request diff found at {pr_diff_url}. Identify any bugs or security vulnerabilities."
    
    # Create the starting state for LangGraph
    initial_state = {
        "messages": [HumanMessage(content=prompt)],
        "iterations": 0
    }
    
    # Fire up the AI engine
    result = agent_app.invoke(initial_state)
    ai_response = result.get("messages")[-1].content
    
    # Format the AI's response for GitHub
    final_comment = f"🤖 **AgenticGit Code Review**\n\n{ai_response}"
    
    # Post the comment back to GitHub
    post_pr_comment(repo_full_name, pr_number, final_comment)

    return {"status": "success", "message": "Code review posted to PR"}