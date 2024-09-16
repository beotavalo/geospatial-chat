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

* LLM: OpenAI
* Knowledge base: This FAQ Knowledge Base was built using data mining and web scrapping from surveying and mapping companies, organizations, and blogs.
* Vector DB: Pinecone
* Embeddings: Sentence Transformers (model: "all-mpnet-base-v2") 
* Monitoring: Grafana
* Interface: Streamlit
* Ingestion pipeline:  Prefect


## Deployment

To run locally execute this command:

```
streamlit run app.py
```
