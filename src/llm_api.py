import os
import requests

def call_llm_model(prompt):
    # Supongamos que tienes una API corriendo para Llama 3.1
    llama_endpoint = os.getenv("LLAMA_API_ENDPOINT")
    
    response = requests.post(
        llama_endpoint,
        json={"prompt": prompt, "max_tokens": 1000}
    )
    
    if response.status_code == 200:
        return response.json()["choices"][0]["text"]
    else:
        return "Error: Failed to call Llama model API"