from utils.llm import call_gemini
from langchain_core.messages import HumanMessage

def writer_node(state):
    """
    Writer agent: Generates the final answer.
    """
    print("--- WRITER ---")
    messages = state['messages']
    last_message = messages[-1]
    
    prompt = f"""You are a technical writer. Summarize the following research into a clear, concise answer.
    Research: {last_message.content}
    """
    
    response = call_gemini(prompt)
    return {"messages": [response]}
