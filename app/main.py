from fastapi import FastAPI
from pydantic import BaseModel
from langchain_core.messages import HumanMessage
from app.agent.graph import agent_app

# Initialize the API
app = FastAPI(title="AgenticGit Engine", description="AI Agent that writes and tests code.")

# Define the expected input payload
class AgentRequest(BaseModel):
    prompt: str

@app.post("/generate")
async def generate_code(request: AgentRequest):
    """
    Takes a user prompt, triggers the LangGraph agent, and returns the verified code.
    """
    # Create the starting state for LangGraph
    initial_state = {
        "messages": [HumanMessage(content=request.prompt)],
        "iterations": 0
    }
    
    # Fire up the AI engine (this will loop until the code works or hits the limit)
    result = agent_app.invoke(initial_state)
    
    # Extract the final results from the state clipboard
    final_code = result.get("current_code", "")
    sandbox_output = result.get("sandbox_result", {})
    
    return {
        "status": "success" if sandbox_output.get("success") else "failed",
        "loops_taken": result.get("iterations"),
        "code_generated": final_code,
        "sandbox_logs": sandbox_output.get("output"),
        "error_logs": sandbox_output.get("error")
    }