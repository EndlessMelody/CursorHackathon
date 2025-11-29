from fastapi import APIRouter, Depends
from pydantic import BaseModel
from langchain_core.messages import HumanMessage
from agents.graph import create_graph

router = APIRouter()
graph = create_graph()

class ChatRequest(BaseModel):
    message: str
    project_id: int = 1

@router.post("/")
def chat(request: ChatRequest):
    initial_state = {"messages": [HumanMessage(content=request.message)]}
    result = graph.invoke(initial_state)
    return {"response": result["messages"][-1].content}
