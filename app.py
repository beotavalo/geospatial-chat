import pandas as pd
import streamlit as st
import pandas as pd
import numpy as np
import src.utils as ut
import src.llm_api as llm
import pinecone
import requests
from sentence_transformers import SentenceTransformer
from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec
import time
import numpy as np


#Get API keys from exteral services

openai_api_key = ut.get_openai_api_key()
pinecone_api_key = ut.get_pinecone_api_key()
# Setting up Vector DB
INDEX_NAME = "geo-kowledge-base"
# Initialize Pinecone
pc = Pinecone(api_key=pinecone_api_key)
# Check if the index exists before trying to create it
if not pc.has_index(INDEX_NAME):
    pc.create_index(
        name=INDEX_NAME,
        dimension=768,
        metric="cosine",
        spec=ServerlessSpec(
            cloud='aws', 
            region='us-east-1'
        ) 
    )  
else:
    print(f"Index {INDEX_NAME} already exists.")

# Wait for the index to be ready
while not pc.describe_index(INDEX_NAME).status['ready']:
    time.sleep(1)
    
index = pc.Index(INDEX_NAME)

def readData(data_path):
    #Load the dataset
    try:
        df = pd.read_csv('/workspaces/geospatial-chat/data/processed/train_data.csv')
    except FileNotFoundError:
        raise Exception("The 'train_data.csv' file was not found within folder 'data/'.")
    return df

def store_podcast_vectors_in_pinecone(df):
    # Cargar modelo de embeddings
    model = SentenceTransformer("all-mpnet-base-v2")

    # Concatenar título y descripción
    df['document'] = df['question'] + " " + df['text']
    
    # Generar embeddings
    kb_vectors = model.encode(df['document'], batch_size=16, show_progress_bar=True)

        # Almacenar los vectores en Pinecone
    for idx, vector in enumerate(kb_vectors):
        pinecone_id = str(df['id'].iloc[idx])
        question = str(df['question'].iloc[idx])
        area = str(df['area'].iloc[idx])
        text = str(df['text'].iloc[idx])
        index.upsert(vectors=[{"id": pinecone_id,"values": vector,"metadata": {"question": question, "area": area, 'text':text}}])


    print("Vector DB created on Pinecone")

# Función para recuperar el contexto relevante
def get_context_from_pinecone(user_query):
    model = SentenceTransformer("all-mpnet-base-v2")
    query_vector = model.encode(user_query)  # Función que embebe la query
    results = index.query(queries=[query_vector], top_k=5)
    context = " ".join([result['text'] for result in results['matches']])
    return context


#Main

def main():
    data_path = '/workspaces/geospatial-chat/data/processed/train_data.csv'
    df = readData(data_path )
    store_podcast_vectors_in_pinecone(df)

    st.title("Geospatial Chat - ACME")
    user_query = st.text_input("Enter your query")
    if user_query:
        # Recuperar contexto de Pinecone
        context = get_context_from_pinecone(user_query)

        # Crear el prompt para Llama
        prompt = ut.create_prompt(user_query, context)
    
        # Enviar el prompt al modelo Llama
        #response = llm.call_llama_model(prompt)
        response = 'Development my response'

        #Show RAG answer
        st.write(f"Model Response: {response}")

if __name__ == "__main__":
    main()