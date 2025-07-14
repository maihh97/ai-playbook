import os
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain.prompts import ChatPromptTemplate

# Load environment variables from .env file
load_dotenv()

# Azure OpenAI Authentication from .env file 
endpoint = os.getenv("AOAI_ENDPOINT")
api_key = os.getenv("AOAI_API_KEY")
deployment = os.getenv("AOAI_DEPLOYMENT_NAME")
version = os.getenv("AOAI_API_VERSION")

# Initialize Azure OpenAI client
llm = AzureChatOpenAI(
    azure_deployment=deployment,
    api_key=api_key,
    api_version=version,   
    azure_endpoint=endpoint,
)

# Prompt template
prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are an experienced travel planner that provides transportation advice from {origin} to {destination}. Give the user 3 options for transportation, including the estimated time and cost for each option.",
    ),
    ("human", "What is the best way to travel from {origin} to {destination}?"),
]
)

# Create a chain that uses the prompt and the LLM
chain = prompt | llm

# Invoke the chain with various inputs
response = chain.invoke(
    {
        "origin": "Paris",
        "destination": "London",
    }
)

print(response.content)