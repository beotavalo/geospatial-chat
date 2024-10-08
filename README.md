[![Stremalite](https://img.shields.io/badge/-Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![OpenAI](https://img.shields.io/badge/OpenAI-00A3E0?logo=OpenAI&logoColor=white)](https://openai.com/)
[![Python](https://img.shields.io/badge/python-3.x-brightgreen.svg)](https://www.python.org/)

[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![Terraform](https://img.shields.io/badge/terraform-%235835CC.svg?style=for-the-badge&logo=terraform&logoColor=white)](https://www.terraform.io/)
[![GitHub Actions](https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white)](https://docs.github.com/en/actions)


This project is part of LLM Zoomcamp by [DataTalksClub](https://github.com/DataTalksClub/llm-zoomcamp) in the 2024 cohort.

## Problem description
The project involves developing a Retrieval-Augmented Generation (RAG) system with a Large Language Model (LLM) for a FAQ system intended for ACME, a company specializing in Surveying, Mapping, Remote Sensing, and GIS. The aim is to enhance customer service, achieve better client engagement, improve client retention, and reduce response times for inquiries and quotations. A comprehensive Knowledge Base has been constructed through data mining and web scraping to support this.
## Technologies
This is the technological stack used for this project:

* LLM: OpenAI(gpt-3.5-turbo)
* Knowledge base: The Knowledge Base was built using data mining and web scrapping from surveying and mapping companies, organizations, and blogs.
* Vector DB: Pinecone
* Embeddings: Sentence Transformers (model: "all-mpnet-base-v2") 
* Monitoring: Grafana
* Interface: Streamlit
* Ingestion pipeline:  Prefect

## RAG Flow
The [Knowledge Base](https://github.com/beotavalo/geospatial-chat/blob/main/data/processed/train_data.json) was built using data mining and web scrapping from surveying and mapping companies, organizations, and blogs.
We built a vector DB on Pinecone, for embeddings We used Sentence Transformers (model: "all-mpnet-base-v2"), a vector of lenght 768, with metadata.

![](https://github.com/beotavalo/geospatial-chat/blob/main/images/VectorDB.jpg)
![Knowledge Base - Vector DB](https://github.com/beotavalo/geospatial-chat/blob/main/images/Vector%20DB.jpg)

A [query promt](https://github.com/beotavalo/geospatial-chat/blob/main/src/utils.py) with vector DB context is sent to OpenAI LLM model (gpt-3.5-turbo).
```
def call_llm_apenai_model(prompt):
    response = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.choices[0].message.content
```
## Interface
The user can write a query on a Streamit UI, so the chat will deliver a response using Knowledge Base context and LLM query.

![Streamlit -RAG UI](https://github.com/beotavalo/geospatial-chat/blob/main/images/UI-chat2.jpg)

## Deployment

To run locally execute this command:

```
streamlit run app.py
```
