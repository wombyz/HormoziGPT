import os
import requests
import streamlit as st
from termcolor import colored
from dotenv import load_dotenv

import openai
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain.schema import HumanMessage
from render import bot_msg_container_html_template, user_msg_container_html_template, render_article_preview
from utils import semantic_search
import prompts

load_dotenv()

# Set up OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Define chat history storage
if "history" not in st.session_state:
    st.session_state.history = []

# Construct messages from chat history
def construct_messages(history):
    messages = [{"role": "system", "content": prompts.system_message}]
    
    for entry in history:
        role = "user" if entry["is_user"] else "assistant"
        messages.append({"role": role, "content": entry["message"]})
    
    return messages

# Generate response to user prompt
def generate_response():
    st.session_state.history.append({
        "message": st.session_state.prompt,
        "is_user": True
    })

    # Perform semantic search and format results
    search_results = semantic_search(st.session_state.prompt, top_k=3)
    context = ""
    for i, (title, transcript) in enumerate(search_results):
        context += f"Snippet from: {title}\n {transcript}\n\n"

    # Generate human prompt template and convert to API message format
    query_with_context = prompts.human_template.format(query=st.session_state.prompt, context=context)

    # Convert chat history to a list of messages
    messages = construct_messages(st.session_state.history)
    messages.append({"role": "user", "content": query_with_context})

    # Run the LLMChain
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
    print(messages)

    # Parse response
    bot_response = response["choices"][0]["message"]["content"]
    st.session_state.history.append({
        "message": bot_response,
        "is_user": False
    })

# User input prompt
user_prompt = st.text_input("Enter your prompt:",
                            key="prompt",
                            placeholder="e.g. 'Why is Tesla selling off?'",
                            on_change=generate_response
                            )

# Display chat history
for message in st.session_state.history:
    if message["is_user"]:
        st.write(user_msg_container_html_template.replace("$MSG", message["message"]), unsafe_allow_html=True)
    else:
        st.write(bot_msg_container_html_template.replace("$MSG", message["message"]), unsafe_allow_html=True)
