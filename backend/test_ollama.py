from langchain_community.chat_models import ChatOllama
from langchain_core.messages import HumanMessage

try:
    print("Initializing ChatOllama with deepseek-r1:1.5b...")
    llm = ChatOllama(model="deepseek-r1:1.5b")
    
    print("Invoking model...")
    response = llm.invoke([HumanMessage(content="Hello, are you working?")])
    
    print("Response received:")
    print(response.content)
except Exception as e:
    print(f"Error: {e}")
