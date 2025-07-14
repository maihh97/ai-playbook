# Getting started

1. Create an Azure OpenAI Service via Azure Portal
- Note down Azure OpenAI endpoint in .env file
- Note down Azure OpenAI api_key .env file
2. Go to Azure AI Foundry (ai.azure.com) and review models in Model Catalogue
3. Deploy a model 
- Note down the model deployment name (usually the model name) in .env file
4. Install chainlit
      ```bash
      pip install chainlit
      ```
5. Run chainlit command
      ```bash
      chainlit run app.py
      ```