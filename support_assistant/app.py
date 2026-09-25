from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from support_graph import support_app

app = FastAPI(title="Zepto Customer Support Assistant", description="Agentic RAG microservice powered by LangGraph & ChromaDB", version="1.0.0")

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    category: str
    context: str
    response: str

@app.get("/")
def root():
    return {"status": "ok", "message": "Zepto Support Assistant API is running."}

@app.post("/query", response_model=QueryResponse)
def handle_query(request: QueryRequest):
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query string cannot be empty.")
    initial_state = {"query": request.query}
    result = support_app.invoke(initial_state)
    return QueryResponse(category=result.get('category', 'general'), context=result.get('context', ''), response=result.get('response', ''))
