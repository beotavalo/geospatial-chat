import pandas as pd
import streamlit as st
import pandas as pd
import numpy as np
from typing import List
import src.utils as ut
import src.llm_api as llm
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
        df = pd.read_csv('data/processed/train_data.csv')
    except FileNotFoundError:
        raise Exception("The 'train_data.csv' file was not found within folder 'data/'.")
    return df
def unified_store_podcast_vectors(df: pd.DataFrame):

    # Load embeddings model
    model = SentenceTransformer("all-mpnet-base-v2")

    # Concatenate  Title and Description
    df['document'] = df['question'] + " " + df['text']

    # Process batch registers
    def process_batch(batch: List[pd.Series]):
        ids_to_check = [str(row["id"]) for row in batch]
        try:
            existing_vectors = index.fetch(ids=ids_to_check)["vectors"]
        except Exception as e:
            print(f"Error to get existent vectors: {e}")
            existing_vectors = {}

        new_vectors = []
        for row in batch:
            pinecone_id = str(row["id"])
            if pinecone_id not in existing_vectors:
                vector = model.encode(row["document"])
                new_vectors.append(
                    {
                        "id": pinecone_id,
                        "values": vector.tolist(),
                        "metadata": {
                            "question": str(row["question"]), 
                            "area": str(row["area"]),
                            "text": str(row["text"]),
                        },
                    }
                )
            else:
                print(
                    f"Vector with ID {pinecone_id} already exists on Pinecone")

        if new_vectors:
            try:
                index.upsert(vectors=new_vectors)
                print(f"The {len(new_vectors)} upserted on Pinecone")
            except Exception as e:
                print(f"Error storaging new vectors: {e}")

    # Procesar el DataFrame en lotes
    batch_size = 100  # Ajusta este valor según tus necesidades
    for i in range(0, len(df), batch_size):
        batch = df.iloc[i: i + batch_size]
        process_batch(batch.to_dict("records"))

    print("Completed process")

# Función para recuperar el contexto relevante
def get_context_from_pinecone(user_query):
    model = SentenceTransformer("all-mpnet-base-v2")

    
    query_vector = model.encode(user_query).tolist()  
    results = index.query(vector=query_vector, top_k=1, include_metadata=True)

    context = []
    for match in results["matches"]:
        # Check if 'metadata' exist and y contains 'title'
        if "metadata" in match and "text" in match["metadata"]:
            context.append(match["metadata"]["text"])
        else:
            # in case the 'title' doesn exist, use the ID as fallback
            context.append(f"Document ID: {match['id']}")

    
    return context
   

#Main
def main():
    data_path = 'data/processed/train_data.csv'
    df = readData(data_path )
    unified_store_podcast_vectors(df)
   
    st.title("Geospatial Chat - ACME")
    user_query = st.text_input("Enter your query")
    if user_query:
        # Recuperar contexto de Pinecone
        context = get_context_from_pinecone(user_query)

        # Crear el prompt para Llama
        prompt = ut.create_prompt(user_query, context)
    
        # Enviar el prompt al modelo Llama
        response = llm.call_llm_apenai_model(prompt)
        #response = 'Development my response'

        #Show RAG answer
        st.write(f"Response: {response}")

if __name__ == "__main__":
    main()