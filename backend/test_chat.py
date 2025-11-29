import requests
import json

try:
    response = requests.post(
        "http://localhost:8000/api/v1/chat/",
        json={"message": "hello", "project_id": 1},
        timeout=10
    )
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
