from openai import AsyncAzureOpenAI
import chainlit as cl
import os
from dotenv import load_dotenv
import webbrowser

# Load environment variables from .env file
load_dotenv()

# Azure OpenAI Authentication from .env file 
endpoint = os.getenv("AOAI_ENDPOINT")
api_key = os.getenv("AOAI_API_KEY")
deployment = os.getenv("AOAI_DEPLOYMENT_NAME")

# Initialize Azure OpenAI client
client = AsyncAzureOpenAI(
    azure_endpoint=endpoint,
    api_key=api_key,
    api_version="2025-01-01-preview"
)

# Optional - define Chainlit action to open its documentation
@cl.action_callback("action_button")
async def on_action(action: cl.Action):
    url = "https://docs.chainlit.io"  # Replace with your desired URL
    webbrowser.open_new_tab(url)

# Define message to appear at the start of the chat session
@cl.on_chat_start
async def start_chat():
    cl.user_session.set(
        "message_history",
        [{"role": "system", "content": "You are a helpful assistant who answers user queries."}],
    )
    actions = [
        cl.Action(
            name="action_button",
            icon="mouse-pointer-click",
            payload={"value": "example_value"},
            label="Link to Documentation"
        )
    ]
    await cl.Message(content="Hello, get started by entering your prompt below or review Chainlit documentation by clicking the link", actions=actions).send()

# Handle user prompt
@cl.on_message
async def on_message(message: cl.Message):
    message_history = cl.user_session.get("message_history")
    message_history.append({"role": "user", "content": message.content})
    
    msg = cl.Message(content="")
    
    async for stream_resp in await client.chat.completions.create(
        model=deployment,
        messages=message_history,
        stream=True,
    ):
        if stream_resp and len(stream_resp.choices) > 0:
            token = stream_resp.choices[0].delta.content or ""
            await msg.stream_token(token)
            
    message_history.append({"role": "assistant", "content": msg.content})
    await msg.send()