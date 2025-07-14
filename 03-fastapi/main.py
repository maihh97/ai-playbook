import os
from dotenv import load_dotenv

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import uvicorn

from pydantic import BaseModel
from openai import AsyncAzureOpenAI, AzureOpenAI

load_dotenv()

# Initialise FastAPI client
app = FastAPI()

# Azure OpenAI Authentication from .env file 
endpoint = os.getenv("AOAI_ENDPOINT")
api_key = os.getenv("AOAI_API_KEY")
deployment = os.getenv("AOAI_DEPLOYMENT_NAME")

client_stream = AsyncAzureOpenAI(
    azure_endpoint=endpoint,
    api_key=api_key,
    api_version="2025-01-01-preview"
)

client = AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=api_key,
    api_version="2025-01-01-preview"
)

# Prompt class using pydantic BaseModel
class UserPrompt(BaseModel):
    input: str
    
# Generate Stream
# Streaming allows you to see the response as it's being generated:
async def stream_processor(response):
    async for chunk in response:
        if len(chunk.choices) > 0:
            delta = chunk.choices[0].delta
            if delta.content:
                yield delta.content

# API Endpoint for Streaming
@app.post("/stream")
async def stream(prompt: UserPrompt):
    try:
        azure_open_ai_response = await client_stream.chat.completions.create(
            model=deployment,
            messages=[{"role": "user", "content": prompt.input}],
            stream=True
        )
        return StreamingResponse(stream_processor(azure_open_ai_response), media_type="text/event-stream")
    except Exception as e:
        return {"error": str(e)}
    
# API Endpoint for Normal Response
@app.post("/getresponse")
def get_response(prompt: UserPrompt):
    try:
        response = client.chat.completions.create(
            model=deployment,
            messages=[{"role": "user", "content": prompt.input}]
        )
        return {"response": response.choices[0].message.content}
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000)