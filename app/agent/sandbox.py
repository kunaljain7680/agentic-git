import docker
import os
from dotenv import load_dotenv

# Load our .env file so we can access SANDBOX_MEM_LIMIT
load_dotenv()

def run_in_sandbox(code_string: str) -> dict:
    """
    Spins up an ephemeral Docker container to execute AI-generated code.
    Returns a dictionary containing the success status and the execution logs.
    """
    # Connect to the Docker Desktop engine running on your machine
    client = docker.from_env()
    mem_limit = os.getenv("SANDBOX_MEM_LIMIT", "512m")
    
    try:
        # Spin up the burner container
        logs = client.containers.run(
            image="python:3.10-slim",
            command=["python", "-c", code_string],
            mem_limit=mem_limit,
            network_disabled=True, # ZERO-TRUST: The AI code cannot access the internet
            remove=True,           # Auto-destroy the container the second it finishes
            stderr=True,
            stdout=True
        )
        
        # If the code runs perfectly (Exit Code 0), it reaches here
        return {
            "success": True,
            "output": logs.decode("utf-8"),
            "error": None
        }
        
    except docker.errors.ContainerError as e:
        # If the code crashes (e.g., SyntaxError, AssertionError), Docker throws this error.
        # We catch it and return the stack trace so the AI can read it and fix its mistakes.
        return {
            "success": False,
            "output": e.stderr.decode("utf-8") if e.stderr else "Unknown crash",
            "error": "Execution failed"
        }
    except Exception as e:
        # Catch-all for Docker Engine issues (e.g., Docker Desktop isn't running)
        return {
            "success": False,
            "output": "",
            "error": str(e)
        }