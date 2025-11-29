import requests
import json

try:
    print("Testing Ollama API via HTTP...")
    
    url = "http://localhost:11434/api/chat"
    data = {
        "model": "deepseek-r1:1.5b",
        "messages": [
            {
                "role": "user",
                "content": "Hello"
            }
        ],
        "stream": False
    }
    
    print(f"Sending request to {url} with model deepseek-r1:1.5b...")
    response = requests.post(url, json=data, timeout=30)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")

except Exception as e:
    print(f"Error: {e}")
