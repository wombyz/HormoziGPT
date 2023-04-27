from render import bot_msg_container_html_template, user_msg_container_html_template, render_article_preview
import prompts
from utils import semantic_search
import openai
import os
import requests
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import (
    HumanMessage,
)
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
import streamlit as st

openai.api_key = os.environ["OPENAI_API_KEY"]

st.title("HormoziGPT")

def construct_messages(history):
    messages = [{"role": "system", "content": prompts.system_message}]
    
    for entry in history:
        role = "user" if entry["is_user"] else "assistant"
        messages.append({"role": role, "content": entry["message"]})
    
    return messages

if "history" not in st.session_state:
    st.session_state.history = []


def generate_response():

    st.session_state.history.append({
        "message": st.session_state.prompt,
        "is_user": True
    })

    # Perform semantic search
    search_results = semantic_search(st.session_state.prompt, top_k=3)

    # Format search results
    context = ""
    for i, (title, transcript) in enumerate(search_results):
        context += f"Snippet from: {title}\n {transcript}\n\n"

    # Insert user query and context into human prompt template
    query_with_context = prompts.human_template.format(query=st.session_state.prompt, context=context)

    # Convert to API message format
    human_message_prompt = HumanMessagePromptTemplate.from_template(query_with_context)

    # Convert chat history to a list of messages
    messages = construct_messages(st.session_state.history)

    # Add the user message to the chat history
    messages.append(human_message_prompt)

    # Run the LLMChain
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    # Parse response
    bot_response = response["choices"][0]["message"]["content"]

    st.session_state.history.append({
        "message": bot_response,
        "is_user": False
    })

st.text_input("Enter your prompt:",
              key="prompt",
              placeholder="e.g. 'Why is Tesla selling off?'",
              on_change=generate_response
              )

for message in st.session_state.history:
    if message["is_user"]:
        st.write(user_msg_container_html_template.replace(
            "$MSG", message["message"]), unsafe_allow_html=True)
    else:
        st.write(bot_msg_container_html_template.replace(
            "$MSG", message["message"]), unsafe_allow_html=True)

# Your existing code for API keys, environment variables, and utility functions
