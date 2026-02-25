from app.core.langgraph.agent import agent_executor

def main():
    print("=== InferHealth Production Agent Ready ===")
    
    initial_state = {
        "query": "What are the symptoms of HIV virus?",
        "last_agent_response": "",
        "tool_observations": [],
        "num_steps": 0,
        "user_location": ""
    }
    
    # Run the agent
    final_state = agent_executor.invoke(initial_state)
    
    print("\n--- FINAL ANSWER ---")
    print(final_state.get("last_agent_response"))

if __name__ == "__main__":
    main()
