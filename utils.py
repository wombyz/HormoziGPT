import os
import openai
import requests
import streamlit as st


openai.api_key = st.secrets["OPENAI_API_KEY"]
api_key_pinecone = st.secrets["PINECONE_API_KEY"]
pinecone_environment = st.secrets["PINECONE_ENVIRONMENT"]
pinecone_endpoint = st.secrets["PINECONE_ENDPOINT"]

# Get embeddings for a given string
def get_embeddings_openai(text):
    response = openai.Embedding.create(
        input=text,
        model="text-embedding-ada-002"
    )
    response = response['data']

    # extract embeddings from responses0
    return [x["embedding"] for x in response]

# Search Pinecone for similar documents
def semantic_search(query, **kwargs):
    # Embed the query into a vector
    xq = get_embeddings_openai(query)

    # Call Pinecone's REST API
    url = pinecone_endpoint
    headers = {
        "Api-Key": api_key_pinecone,
        "Content-Type": "application/json"
    }
    body = {
        "vector": xq[0],
        "topK": str(kwargs["top_k"]) if "top_k" in kwargs else "1",
        "includeMetadata": "false" if "include_metadata" in kwargs and not kwargs["include_metadata"] else True
    }
    try:
        res = requests.post(url, json=body, headers=headers)
        res.raise_for_status()  # Raise an exception if the HTTP request returns an error
        res = res.json()
        titles = [r["metadata"]["title"] for r in res["matches"]]
        transcripts = [r["metadata"]["transcript"] for r in res["matches"]]
        return list(zip(titles, transcripts))
    except Exception as e:
        print(f"Error in semantic search: {e}")
        raise
