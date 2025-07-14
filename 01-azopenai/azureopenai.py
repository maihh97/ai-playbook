import os
from dotenv import load_dotenv
from openai import AzureOpenAI, AsyncAzureOpenAI

# Load environment variables from .env file
load_dotenv()

# Azure OpenAI Authentication from .env file 
endpoint = os.getenv("AOAI_ENDPOINT")
api_key = os.getenv("AOAI_API_KEY")
deployment = os.getenv("AOAI_DEPLOYMENT_NAME")

# Initialize Azure OpenAI client
client = AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=api_key,  
    api_version="2025-01-01-preview"
)

# If use streaming capabilities, initialize an async client
client_stream = AsyncAzureOpenAI(
    azure_endpoint=endpoint,
    api_key=api_key,
    api_version="2025-01-01-preview"
)

# 3 roles in a chat history
messages=[
    # System message - sets model behavior and context
    {"role": "system", "content": "You are a singer who answers user queries in songs."},
    
    # User messages - user inputs to the model
    {"role": "user", "content": "Hello, how are you today?"},
    
    # Assistant messages - previous responses from the model if any
    {"role": "assistant", "content": "🎶 Oh, thank you for asking, I'm feeling quite alright, Here to help you out, from morning until night. With melodies and answers, I'll make your day bright, So tell me what you need, and I'll sing it with delight. 🎶"},
]

# Call the Azure OpenAI model
response = client.chat.completions.create(
    model=deployment,
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Write a poem about the sea."}
    ]
    # temperature=0.8 # Optional: controls randomness of output
    # top_p=0.9,  # Optional: controls diversity of output
    # max_tokens=100,  # Optional: limits the length of the response
    # frequency_penalty=0.5,  # Optional: discourages repetition
    # presence_penalty=0.5,  # Optional: encourages new topics
    # stop=["\n"],  # Optional: specifies stop sequences
    # stream=True,  # Optional: enables streaming responses
    # tools=[{"type": "function", "function": {"name": "get_weather", "description": "Get real-time weather updates"}}],  # Optional: defines callable tools
    # extra_body={
    # "data_sources": [
    #     {
    #         "type": "azure_search",
    #         "parameters": {
    #         "endpoint": search_endpoint,
    #         "index_name": search_index_name,
    #         "authentication": {
    #             "type": "system_assigned_managed_identity"
    #         }}}]
    # } # Optional: RAG using Azure AI Search https://learn.microsoft.com/en-us/azure/ai-foundry/openai/references/on-your-data?tabs=python
)

# Print the response and token usage
print(f"Response: {response.choices[0].message.content}") 
print(f"Prompt tokens: {response.usage.prompt_tokens}")
print(f"Completion tokens: {response.usage.completion_tokens}")
print(f"Total tokens: {response.usage.total_tokens}")