import json

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from contextlib import asynccontextmanager

from api.rag_pipeline import RagPipeline

# Initialize RAG pipeline
@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.rag = RagPipeline()
    yield

app = FastAPI(lifespan= lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins= ["http://localhost:5173"],
    allow_credentials= True,
    allow_methods= ["*"],
    allow_headers= ["*"]
)

class ChatRequest(BaseModel):
    question: str
    
@app.post("/chat/stream")
def chat(request: ChatRequest):
    question = request.question.strip()
    
    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    
    rag = app.state.rag
    try:
        result = rag.retrieve(question)
        prompt = rag.build_prompt(result)
    
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Retrieval error  \n{exc}")
    
    def generate():
        try:
            for token in rag.stream_answer(prompt):
                yield json.dumps({
                    "type": "token",
                    "text": token
                }) + "\n"
            
            yield json.dumps({
                "type": "done"
            }) + "\n"
        
        except Exception as exc:
            yield json.dumps({
                "type": "error",
                "message": str(exc)
            }) + "\n"
    
    return StreamingResponse(
        generate(),
        media_type="application/x-ndjson",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no"
        }
    )