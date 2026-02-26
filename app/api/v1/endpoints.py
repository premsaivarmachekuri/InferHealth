from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.core.agents.agent import agent_executor

app = FastAPI(title="InferHealth API", version="1.0.0")

class AgentQuery(BaseModel):
    query: str

class AgentResponse(BaseModel):
    response: str
    steps: int

@app.get("/")
def root():
    return {"message": "InferHealth API is online. Use /v1/chat for agent queries."}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/v1/chat", response_model=AgentResponse)
def chat(request: AgentQuery):
    """
    Synchronous route for the blocking agent call.
    In production, this would use a task queue like Celery or a background thread.
    """
    try:
        initial_state = {
            "query": request.query,
            "last_agent_response": "",
            "tool_observations": [],
            "num_steps": 0,
            "user_location": ""
        }
        # invoke is a blocking call
        result = agent_executor.invoke(initial_state)
        
        return AgentResponse(
            response=result["last_agent_response"],
            steps=result["num_steps"]
        )
    except Exception as e:
        print(f"API Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Agent Error: {str(e)}")
