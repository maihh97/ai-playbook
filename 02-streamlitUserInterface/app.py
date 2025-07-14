import streamlit as st
import os
from openai import AzureOpenAI
from dotenv import load_dotenv
import tiktoken

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

# Streamlit app title
st.title("LLM Streamlit App")

default_prompt = """
You are an AI assistant that helps financial advisors to review information about the company finance product. 
"""

# Session state to store chat messages
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": default_prompt},
        {"role": "assistant", "content": "Hello, can I help you?"}
    ]
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Start the chat session
if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    
    # Generate completion
    response = client.chat.completions.create(
        model=deployment, 
        messages=st.session_state.messages,
    )
    msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)

# Explain tokens
with st.popover("More on Tokens"):
    
    st.markdown('''
        Tokenization involves breaking down text into smaller units, known as tokens, which can be words, subwords, or characters.
        Tiktoken is a fast and efficient tokenization library developed by OpenAI.
    ''')
    encoding_model = st.radio(
        "Set encoding models 👇",
        ["o200k_base", "cl100k_base", "p50k_base", "r50k_base"],
        key="visibility",
        horizontal=True,
    )
    tokenizer = tiktoken.get_encoding(encoding_model)
    text_to_encode = st.text_input("Enter text:")
    encode_btn = st.button("Tokenize")
    if encode_btn:
        encoded_text = tokenizer.encode(text_to_encode)
        st.write("Encoded text:", encoded_text)
        st.write("Token length:", len(encoded_text))