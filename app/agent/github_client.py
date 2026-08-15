import os
from github import Github
from dotenv import load_dotenv

load_dotenv()

def get_pr_diff_content(repo_full_name: str, pr_number: int) -> str:
    """Fetches the code diff / patches from a PR."""
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        return "Error: GITHUB_TOKEN is not set."
    try:
        g = Github(token)
        repo = g.get_repo(repo_full_name)
        pr = repo.get_pull(pr_number)
        diff_text = ""
        for file in pr.get_files():
            diff_text += f"\n--- File: {file.filename} ---\n"
            diff_text += file.patch if file.patch else "[No patch]"
        return diff_text
    except Exception as e:
        return f"Failed to fetch PR diff: {e}"

def post_pr_comment(repo_full_name: str, pr_number: int, comment_body: str):
    """Posts a comment on a specific Pull Request."""
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        print("Error: GITHUB_TOKEN is not set.")
        return
    try:
        g = Github(token)
        repo = g.get_repo(repo_full_name)
        pr = repo.get_pull(pr_number)
        pr.create_issue_comment(comment_body)
        print(f"Successfully posted comment to PR #{pr_number}")
    except Exception as e:
        print(f"Failed to post to GitHub: {e}")

def get_raw_file_content(repo_full_name: str, branch_name: str, file_path: str) -> str:
    """Downloads the actual raw Python file from the GitHub PR branch so it can be executed."""
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        return ""
    try:
        g = Github(token)
        repo = g.get_repo(repo_full_name)
        # Pulls the executable raw code, not the patch/diff!
        file_content = repo.get_contents(file_path, ref=branch_name)
        return file_content.decoded_content.decode("utf-8")
    except Exception as e:
        print(f"Failed to fetch raw file: {e}")
        return ""

def update_file_in_pr(repo_full_name: str, branch_name: str, file_path: str, new_content: str, commit_message: str):
    """Commits and pushes fixed code directly back to the PR branch on GitHub."""
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        print("Error: GITHUB_TOKEN is not set.")
        return
    try:
        g = Github(token)
        repo = g.get_repo(repo_full_name)
        # Get the file's current SHA (required by GitHub API to update a file)
        file_contents = repo.get_contents(file_path, ref=branch_name)
        # Update the file on the specific branch
        repo.update_file(
            path=file_path,
            message=commit_message,
            content=new_content,
            sha=file_contents.sha,
            branch=branch_name
        )
        print(f"Successfully pushed fixed code to branch {branch_name}")
    except Exception as e:
        print(f"Failed to update file on GitHub: {e}")