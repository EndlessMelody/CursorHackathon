import ollama

try:
    print("Listing models...")
    models = ollama.list()
    print(f"Models: {models}")

    print("Generating response with deepseek-r1:1.5b...")
    response = ollama.chat(model='deepseek-r1:1.5b', messages=[
      {
        'role': 'user',
        'content': 'Why is the sky blue?',
      },
    ])
    print("Response received:")
    print(response['message']['content'])
except Exception as e:
    print(f"Error: {e}")
