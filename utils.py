import os
import openai
import requests
import streamlit as st
import json

openai.api_key = st.secrets["OPENAI_API_KEY"]
api_key_pinecone = st.secrets["PINECONE_API_KEY"]
pinecone_environment = st.secrets["PINECONE_ENVIRONMENT"]
pinecone_endpoint = st.secrets["PINECONE_ENDPOINT"]

def get_embeddings_openai(text):
    try:
        response = openai.Embedding.create(
            input=text,
            model="text-embedding-ada-002"
        )
        response = response['data']
        return [x["embedding"] for x in response]
    except Exception as e:
        print(f"Error in get_embeddings_openai: {e}")
        raise

def semantic_search(query, **kwargs):
    try:
        xq = get_embeddings_openai(query)

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
        res = requests.post(url, json=body, headers=headers)
        res.raise_for_status()  # Raise an exception if the HTTP request returns an error

        # Ensure the response is valid JSON before parsing it
        try:
            res_json = res.json()
        except json.JSONDecodeError:
            print(f"Invalid JSON response: {res.text}")
            raise

        titles = [r["metadata"]["title"] for r in res_json["matches"]]
        transcripts = [r["metadata"]["transcript"] for r in res_json["matches"]]
        return list(zip(titles, transcripts))

    except Exception as e:
        print(f"Error in semantic_search: {e}")
        raise
