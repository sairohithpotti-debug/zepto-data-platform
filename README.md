# Zepto Data Platform & Customer Support Assistant

An end-to-end Capstone project integrating data analytics, ETL data pipelines, and a Retrieval-Augmented Generation (RAG) AI customer support assistant for Zepto quick-commerce operations.

---

## 📁 Repository Structure

* *analytics/* — Exploratory Data Analysis (EDA), SQL queries, and business insights dashboard.
* *data_pipeline/* — Automated ETL data processing pipeline and pipeline workflows.
* *support_assistant/* — RAG-based Customer Support Assistant built with FastAPI, LangGraph, and ChromaDB.

---

## 💡 Module Summaries & Design Decisions

### *Module 1: Analytics*
* *Summary:* Performs Exploratory Data Analysis (EDA) on Zepto sales, order fulfillment, and customer behavior datasets to derive actionable operational insights.
* *Design Decisions:* Built modular SQL scripts and Python visualization pipelines to analyze delivery latency bottlenecks, order densities, and revenue metrics cleanly.
* *Execution:*
  ```bash
  cd analytics
  python -m notebook
### Module 2: Data Pipeline
Summary: Automated ETL data processing pipeline designed to ingest, clean, transform, and load raw operational data into structured analytical models.
 Design Decisions: Implemented strict schema validation, exception logging, and modular transformation functions to handle edge cases and missing fields reliably.


### Module 3: Customer Support Assistant (RAG)
* Summary: Intelligent support assistant leveraging LangGraph stateful routing, ChromaDB vector retrieval, and FastAPI endpoints to resolve policy queries.
* Design Decisions: Leveraged open-source local embeddings (all-MiniLM-L6-v2) and rule-assisted category classification to provide fast, deterministic policy responses without relying on paid external APIs.
* Execution:
1.	Navigate to the directory and install dependencies:
2.	Start the local FastAPI server using Uvicorn:
3.	Access the interactive Swagger UI in your browser at http://127.0.0.1:8001/docs.
⚙️ Setup & Dependencies
* Python Version: 3.10+
* Core Libraries: FastAPI, Uvicorn, LangGraph, ChromaDB, Sentence-Transformers, Pandas, NumPy (<2.0.0).
