# Zepto Data Platform & Customer Support Assistant

An end-to-end Capstone project integrating data analytics, ETL data pipelines, and a Retrieval-Augmented Generation (RAG) AI customer support assistant for Zepto quick-commerce operations.

---

## 📁 Repository Structure

* *analytics/* — Exploratory Data Analysis (EDA), SQL queries, and business insights dashboard.
* *data_pipeline/* — Automated ETL data processing pipeline and pipeline workflows.
* *support_assistant/* — RAG-based Customer Support Assistant built with FastAPI, LangGraph, and ChromaDB.

---

## 🚀 Module 3: RAG Support Assistant Setup

The support assistant uses *LangGraph* to route queries, *ChromaDB* for vector retrieval across Zepto support policies, and *FastAPI* to expose an interactive API endpoint.

### *1. Installation*
Navigate to the support_assistant directory and install dependencies:
```bash
cd support_assistant
pip install -r requirements.txt
python -m uvicorn app:app --port 8001
[http://127.0.0.1:8001/docs](http://127.0.0.1:8001/docs)
use the post/query endpoint to submit policy questions
