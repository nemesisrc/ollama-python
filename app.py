'''
Local LLM execution using python Ollama module on Windows-->
i. download and install ollama application on windows(pc/laptop).
ii. pull open source models from ollama hub(library/repository).
iii. run LLMs locally for free using python scripts.
'''
import ollama

# initialise the ollama client
client = ollama.Client()

# define model name and input prompt
model = "llama2"
prompt = "What is the capital of France?"

# send the query to the model and get the response
response = client.generate(model=model, prompt=prompt)

# print the response from the model
print("Response from Ollama:")
print(response.response)
