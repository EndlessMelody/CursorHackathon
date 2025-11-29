import os
import google.generativeai as genai
from langchain_core.messages import AIMessage
from dotenv import load_dotenv

load_dotenv()

def call_gemini(prompt: str, model: str = "gemini-2.0-flash-lite-preview-02-05") -> AIMessage:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or "your_api_key_here" in api_key:
        return AIMessage(content="Error: GEMINI_API_KEY not configured. Please check your .env file.")
    
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model)
        response = model.generate_content(prompt)
        return AIMessage(content=response.text)
    except Exception as e:
        return AIMessage(content=f"Error calling Gemini: {str(e)}")
