import os
from dotenv import load_dotenv
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
import asyncio

# Load environment variables from .env file
load_dotenv()

# Azure OpenAI Authentication from .env file 
endpoint = os.getenv("AOAI_ENDPOINT")
api_key = os.getenv("AOAI_API_KEY")
deployment = os.getenv("AOAI_DEPLOYMENT_NAME")

async def main():
    # Initiailize the Kernel
    kernel = Kernel()

    # Create the Azure OpenAI chat completion service
    azure_chat_service = AzureChatCompletion(deployment_name=deployment, api_key=api_key, endpoint=endpoint, service_id="azure_openai_chat")
    # Add the Azure OpenAI chat service to the kernel
    kernel.add_service(azure_chat_service)

    prompt = "How can I travel from Paris to London?"

    result = await kernel.invoke_prompt(prompt)

    print(result)
    
# Run the main function
if __name__ == "__main__":
    asyncio.run(main())