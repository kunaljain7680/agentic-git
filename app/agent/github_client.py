import os
from github import Github
from dotenv import load_dotenv

load_dotenv()

def post_pr_comment(repo_full_name: str, pr_number: int, comment_body: str):
    """
    Authenticates with GitHub and posts a comment on a specific Pull Request.
    """
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        print("Error: GITHUB_TOKEN is not set.")
        return

    try:
        # Initialize the PyGithub client
        g = Github(token)
        
        # Get the repository and the specific PR
        repo = g.get_repo(repo_full_name)
        pr = repo.get_pull(pr_number)
        
        # Post the comment
        pr.create_issue_comment(comment_body)
        print(f"Successfully posted comment to PR #{pr_number} in {repo_full_name}")
        
    except Exception as e:
        print(f"Failed to post to GitHub: {e}")