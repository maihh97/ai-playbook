import os
import gradio as gr
import openai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Azure OpenAI Authentication from .env file 
endpoint = os.getenv("AOAI_ENDPOINT")
api_key = os.getenv("AOAI_API_KEY")
deployment = os.getenv("AOAI_DEPLOYMENT_NAME")

# Initialize Azure OpenAI client
client = openai.AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=api_key,
    api_version="2025-01-01-preview"
)

# Function to get response from OpenAI. We already went through that before. 
def get_response(message, history):
    response = client.chat.completions.create(
        model=deployment,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": message}
        ]
    )
    return response.choices[0].message.content

# Create a Gradio interface for the chatbot
chatbot = gr.ChatInterface(
    fn=get_response,
    type="messages",
    autofocus=False
)

# Launch the chatbot
chatbot.launch() # chatbot.launch(share=True) to have a link to share the interface publicly