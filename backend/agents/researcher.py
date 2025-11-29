from utils.llm import call_gemini

def research_node(state):
    """
    Researcher agent: Searches the vector DB (mocked for now) and summarizes findings.
    """
    print("--- RESEARCHER ---")
    question = state['messages'][-1].content
    
    # TODO: Implement actual RAG retrieval here
    context = "Mock context: The user is asking about " + question
    
    prompt = f"""You are a researcher. Use the following context to answer the question.
    Context: {context}
    Question: {question}
    """
    
    response = call_gemini(prompt)
    return {"messages": [response]}
