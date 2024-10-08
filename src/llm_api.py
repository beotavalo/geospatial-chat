import os
import requests
from openai import OpenAI
import src.utils as ut
openai_api_key = ut.get_openai_api_key()
client = OpenAI(api_key=openai_api_key)


def call_llm_apenai_model(prompt):
    response = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.choices[0].message.content

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