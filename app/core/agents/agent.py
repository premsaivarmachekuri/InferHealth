import json
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END
from app.core.llm_client import get_llm_response
from app.core.prompts.agent_prompts import SYSTEM_PROMPT, TOOLS_DESCRIPTION
from app.core.agents.tools.medical_tools import (
    retrieve_context_tool,
    search_hospital_tool,
    web_search_tool,
    ask_user_tool
)

# === State Schema ===
class AgentState(TypedDict):
    query: str
    last_agent_response: str
    tool_observations: list
    num_steps: int
    user_location: str

# === LLM Node ===
def call_model(state: AgentState) -> dict:
    print(f"\n--- STEP {state.get('num_steps', 0)} ---")
    
    prompt = SYSTEM_PROMPT.format(
        tools_list=TOOLS_DESCRIPTION,
        query=state.get("query", ""),
        tool_observations="\n".join(state.get("tool_observations", []))
    )

    response = get_llm_response(prompt)
    state["last_agent_response"] = response
    state["num_steps"] = state.get("num_steps", 0) + 1
    return state

# === Tool Logic Node ===
def call_tool(state: AgentState) -> dict:
    action_text = state.get("last_agent_response", "")
    
    if "ACTION:" not in action_text:
        state.setdefault("tool_observations", []).append("[Error: No Action specified by LLM]")
        return state

    # Basic parsing logic (could be improved with Regex in production)
    try:
        tool_name = action_text.split("ACTION:")[1].split("\n")[0].strip()
        args_text = "{}"
        if "ARGUMENTS:" in action_text:
            args_text = action_text.split("ARGUMENTS:")[1].strip()
            # Basic JSON extraction
            if "{" in args_text:
                args_text = args_text[args_text.find("{"):args_text.rfind("}")+1]
        
        args = json.loads(args_text)
    except Exception as e:
        state.setdefault("tool_observations", []).append(f"[Error parsing action/args: {str(e)}]")
        return state

    tool_map = {
        "retrieve_context_q_n_a": retrieve_context_tool,
        "search_nearest_hospital": search_hospital_tool,
        "web_search": web_search_tool,
        "ask_user": ask_user_tool
    }

    if tool_name in tool_map:
        try:
            results = tool_map[tool_name](**args)
            state.setdefault("tool_observations", []).append(f"[{tool_name} results: {results['context']}]")
            
            # Special case for location capture
            if tool_name == "ask_user" and "location" in args.get("question", "").lower():
                state["user_location"] = results["context"]
        except Exception as e:
            state.setdefault("tool_observations", []).append(f"[Error executing tool {tool_name}: {str(e)}]")
    else:
        state.setdefault("tool_observations", []).append(f"[Unknown tool: {tool_name}]")

    return state

# === Edge Logic ===
def should_continue(state: AgentState) -> str:
    last_resp = state.get("last_agent_response", "").upper()
    if "ANSWER:" in last_resp or state.get("num_steps", 0) > 10:
        return "end"
    return "continue"

# === Compile Workflow ===
def create_agent():
    workflow = StateGraph(AgentState)
    workflow.add_node("agent", call_model)
    workflow.add_node("tools", call_tool)
    
    workflow.set_entry_point("agent")
    workflow.add_conditional_edges(
        "agent",
        should_continue,
        {"continue": "tools", "end": END}
    )
    workflow.add_edge("tools", "agent")
    
    return workflow.compile()

agent_executor = create_agent()
