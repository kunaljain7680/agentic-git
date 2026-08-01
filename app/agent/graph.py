from langgraph.graph import StateGraph, END
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from app.agent.state import AgentState
from app.agent.sandbox import run_in_sandbox
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize Gemini (Fast, Agentic)
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

def coder_node(state: AgentState):
    """Generates the initial code or rewrites it based on crash logs."""
    messages = state.get("messages", [])
    iterations = state.get("iterations", 0)
    
    # If we have sandbox results, it means the code crashed and we need to fix it
    sandbox_result = state.get("sandbox_result", {})
    if sandbox_result and not sandbox_result.get("success"):
        error_log = sandbox_result.get("output")
        prompt = f"The code crashed. Here is the error log:\n{error_log}\nFix the code and return ONLY valid Python code. No markdown formatting, no explanations."
        messages.append(HumanMessage(content=prompt))
    else:
        # Initial prompt if starting fresh
        system_msg = SystemMessage(content="You are an expert Python engineer. Output ONLY raw, executable Python code. Do not use markdown blocks like ```python. Do not explain the code.")
        if not messages:
             messages = [system_msg, HumanMessage(content="Write a simple python script that prints 'Hello from the secure Docker Sandbox!'")]
    
    # Call Gemini
    response = llm.invoke(messages)
    new_code = response.content.strip()
    
    # Clean up markdown if the AI ignored instructions
    if new_code.startswith("```python"):
        new_code = new_code[9:]
    if new_code.endswith("```"):
        new_code = new_code[:-3]
        
    return {
        "messages": [response], 
        "current_code": new_code.strip(),
        "iterations": iterations + 1
    }

def executor_node(state: AgentState):
    """Takes the code and runs it in the secure Docker sandbox."""
    code = state.get("current_code", "")
    result = run_in_sandbox(code)
    return {"sandbox_result": result}

def route_next_step(state: AgentState):
    """Decides whether to loop back to the AI or finish the job."""
    result = state.get("sandbox_result", {})
    iterations = state.get("iterations", 0)
    
    # Stop condition: Success or too many tries
    if result.get("success") or iterations >= 3:
        return END
    
    # Loop back to fix the bug
    return "coder"

# Build the Graph Architecture
workflow = StateGraph(AgentState)

# Add our two nodes
workflow.add_node("coder", coder_node)
workflow.add_node("executor", executor_node)

# Define the flow
workflow.set_entry_point("coder")
workflow.add_edge("coder", "executor")
workflow.add_conditional_edges("executor", route_next_step)

# Compile the engine
agent_app = workflow.compile()