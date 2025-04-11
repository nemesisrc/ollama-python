# Python Ollama Module Tutorial

Ollama is a tool for running large language models locally. While Ollama itself is primarily a command-line tool, you can interact with it from Python using either the official ollama Python library or by calling its REST API directly.

## Installation

First, make sure you have Ollama installed on your system. Then install the Python package:

```bash
pip install ollama
```

## Basic Usage

### 1. Pulling a Model

Before using a model, you need to pull it:

```python
import ollama

# Pull a model (this downloads it if not already present)
ollama.pull('mistral')
```

### 2. Generating Text

```python
response = ollama.generate(
    model='mistral',
    prompt='Why is the sky blue?'
)

print(response['response'])
```

### 3. Chat Interface

For multi-turn conversations:

```python
response = ollama.chat(
    model='mistral',
    messages=[
        {'role': 'user', 'content': 'Why is the sky blue?'},
    ]
)

print(response['message']['content'])
```

### 4. Streaming Responses

For large responses, you can stream them:

```python
stream = ollama.generate(
    model='mistral',
    prompt='Tell me a long story about a dragon',
    stream=True
)

for chunk in stream:
    print(chunk['response'], end='', flush=True)
```

## Advanced Features

### 1. Customizing Generation Parameters

```python
response = ollama.generate(
    model='mistral',
    prompt='Write a poem about Python',
    options={
        'temperature': 0.7,
        'top_p': 0.9,
        'num_ctx': 2048
    }
)
```

### 2. Listing Available Models

```python
models = ollama.list()
print(models)
```

### 3. Creating Custom Models

You can create custom models by modifying existing ones:

```python
# Create a custom model
ollama.create(
    model='my-mistral',
    modelfile='''
    FROM mistral
    SYSTEM You are a helpful coding assistant that specializes in Python.
    '''
)

# Then use it like any other model
response = ollama.generate(model='my-mistral', prompt='How do I use list comprehensions?')
print(response['response'])
```

### 4. Using the REST API Directly

If you prefer to use the REST API (useful if ollama is running on a different machine):

```python
import requests

response = requests.post(
    'http://localhost:11434/api/generate',
    json={
        'model': 'mistral',
        'prompt': 'Explain quantum computing in simple terms'
    }
)

for line in response.iter_lines():
    if line:
        print(line.decode('utf-8'))
```

## Error Handling

```python
try:
    response = ollama.generate(
        model='non-existent-model',
        prompt='This will fail'
    )
except ollama.ResponseError as e:
    print('Error:', e.error)
    print('Status code:', e.status_code)
```

## Complete Example

Here's a complete example of a simple chatbot:

```python
import ollama

def chat_with_model():
    print("Starting chat with Mistral. Type 'quit' to exit.")
    messages = []
    
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'quit':
            break
            
        messages.append({'role': 'user', 'content': user_input})
        
        response = ollama.chat(
            model='mistral',
            messages=messages,
            stream=True
        )
        
        print("Assistant: ", end='')
        full_response = ''
        for chunk in response:
            part = chunk['message']['content']
            print(part, end='', flush=True)
            full_response += part
        
        messages.append({'role': 'assistant', 'content': full_response})
        print()

if __name__ == "__main__":
    # Ensure the model is available
    try:
        ollama.generate(model='mistral', prompt='test')
    except ollama.ResponseError:
        print("Pulling mistral model...")
        ollama.pull('mistral')
    
    chat_with_model()
```

## Tips

1. Start with smaller models like `mistral` or `llama2` if you have limited resources
2. For better performance, use GPU acceleration if available
3. The first run will be slower as models need to be downloaded
4. You can manage models with `ollama.list()`, `ollama.pull()`, and `ollama.delete()`

Remember that Ollama needs to be running in the background for the Python module to work. You can start it with the `ollama serve` command in your terminal.
