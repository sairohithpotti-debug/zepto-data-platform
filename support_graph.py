import os
import glob
import chromadb
from chromadb.utils import embedding_functions
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, END

script_dir = os.path.dirname(os.path.abspath(__file__))
CHROMA_PATH = os.path.join(script_dir, "chroma_db")
COLLECTION_NAME = "zepto_policies"

embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)
client = chromadb.PersistentClient(path=CHROMA_PATH)
collection = client.get_or_create_collection(
    name=COLLECTION_NAME, embedding_function=embedding_func
)

if collection.count() == 0:
    doc_files = sorted(glob.glob(os.path.join(script_dir, "doc_*.txt")))
    documents, ids, metadatas = [], [], []

    for filepath in doc_files:
        file_id = os.path.basename(filepath)
        with open(filepath, "r", encoding="utf-8") as f:
            documents.append(f.read())
        ids.append(file_id)
        metadatas.append({"source": file_id})

    if documents:
        collection.add(documents=documents, ids=ids, metadatas=metadatas)

class GraphState(TypedDict):
    query: str
    category: str
    context: str
    response: str

def classify_node(state: GraphState) -> GraphState:
    q = state["query"].lower()
    if any(w in q for w in ["deliver", "delay", "late", "time", "fee", "pincode"]):
        category = "delivery"
    elif any(w in q for w in ["return", "refund", "cancel", "damaged", "missing", "wallet"]):
        category = "refund_cancellation"
    elif any(w in q for w in ["pass", "membership", "tier", "subscription"]):
        category = "membership"
    else:
        category = "general"
    return {"category": category}

def retrieve_node(state: GraphState) -> GraphState:
    query = state["query"]
    results = collection.query(query_texts=[query], n_results=2)
    retrieved_texts = results["documents"][0] if results["documents"] else []
    context_str = "\n".join(retrieved_texts)
    return {"context": context_str}

def generate_node(state: GraphState) -> GraphState:
    category = state.get("category", "general")
    context = state.get("context", "")
    if not context:
        ans = "I'm sorry, I couldn't find specific policy details for your request. Please reach out to customer support via in-app chat."
    else:
        ans = f"Based on our {category.replace('_', ' ')} policy:\n\n{context}\n\nFor further assistance, contact our 24/7 in-app support chat."
    return {"response": ans}

workflow = StateGraph(GraphState)
workflow.add_node("classify", classify_node)
workflow.add_node("retrieve", retrieve_node)
workflow.add_node("generate", generate_node)
workflow.set_entry_point("classify")
workflow.add_edge("classify", "retrieve")
workflow.add_edge("retrieve", "generate")
workflow.add_edge('generate', END)
support_app = workflow.compile()
