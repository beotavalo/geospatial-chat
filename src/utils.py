from dotenv import load_dotenv, find_dotenv
import os

def get_openai_api_key():
    _ = load_dotenv(find_dotenv())

    return os.getenv("OPENAI_API_KEY")

def get_pinecone_api_key():
    _ = load_dotenv(find_dotenv())
    return os.getenv("PINECONE_API_KEY")

def create_prompt(user_query, context):
    prompt = f"""
    You are an Surveying, Mapping and Geospatial Expert. Based on the following context, answer the user's query in detail.
    
    Context: {context}
    
    User Query: {user_query}
    
    Please provide a clear, concise, and informative answer.
    """
    return prompt


