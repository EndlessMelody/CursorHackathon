from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated, List
from langchain_core.messages import BaseMessage
import operator

from .researcher import research_node
from .writer import writer_node

class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]

def create_graph():
    workflow = StateGraph(AgentState)
    
    workflow.add_node("researcher", research_node)
    workflow.add_node("writer", writer_node)
    
    workflow.set_entry_point("researcher")
    
    workflow.add_edge("researcher", "writer")
    workflow.add_edge("writer", END)
    
    return workflow.compile()
