from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.core.langgraph.agent import agent_executor

app = FastAPI(title="InferHealth API", version="1.0.0")

class AgentQuery(BaseModel):
    query: str

class AgentResponse(BaseModel):
    response: str
    steps: int

@app.post("/v1/chat", response_model=AgentResponse)
async def chat(request: AgentQuery):
    try:
        initial_state = {
            "query": request.query,
            "last_agent_response": "",
            "tool_observations": [],
            "num_steps": 0,
            "user_location": ""
        }
        result = agent_executor.invoke(initial_state)
        return AgentResponse(
            response=result["last_agent_response"],
            steps=result["num_steps"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    return {"status": "healthy"}
