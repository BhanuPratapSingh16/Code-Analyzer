import json
import shutil
from fastapi import FastAPI, HTTPException, UploadFile, File, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from contextlib import asynccontextmanager
from api.rag_pipeline import RagPipeline
from api.repo_manager import RepositoryManager
from pathlib import Path
import uuid
from config import MAX_UPLOAD_SIZE, CHUNK_SIZE

pipelines = {}
repository_manager = RepositoryManager()

# Initialize RAG pipeline
@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.pipelines = pipelines
    yield

app = FastAPI(lifespan= lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins= ["http://localhost:5173"],
    allow_credentials= True,
    allow_methods= ["*"],
    allow_headers= ["*"]
)

@app.get("/api/rag/connection")
def health_check():
    return {
        "status": "UP",
        "service": "CodeGraph RAG Engine"
    }

class ChatRequest(BaseModel):
    repository_id: str
    question: str
   

async def save_upload(file: UploadFile, destination: Path):
    total_size = 0
    
    destination.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        with destination.open("wb") as output:
            while True:
                chunk = await file.read(CHUNK_SIZE)
                
                if not chunk:
                    break
                
                total_size += len(chunk)
                
                if total_size > MAX_UPLOAD_SIZE:
                    raise ValueError("Upload exceeds 100 MB limit")
                
                output.write(chunk)
            
        return destination
    
    except Exception:
        destination.unlink(missing_ok=True)
        raise

    finally:
        await file.close()


@app.post("/repositories/{repository_id}/upload")
async def upload_repository(repository_id:uuid.UUID, file:UploadFile = File(...)):
    if not file.filename or not file.filename.lower().endswith(".zip"):
        raise HTTPException(status_code=400, detail="Please upload a ZIP repository")
    
    temp_path = Path("storage/temp") / f"{str(uuid.uuid4())}.zip"
    temp_path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        await save_upload(file, temp_path)

        _, storage_path = repository_manager.save(repository_id, temp_path)
        
        rag = RagPipeline(repo_path=storage_path)
        
        app.state.pipelines[str(repository_id)] = rag
        
        return {
            "repository_id": repository_id,
            "status": "READY",
            "message": "Repository indexed successfully!"
        }
    except Exception as exc:
        print(exc)
        raise HTTPException(
            status_code=500,
            detail="Repository upload failed"
        )
        
    finally:
        file.file.close()
        temp_path.unlink(missing_ok=True)
    
@app.post("/chat/stream")
def chat(request: ChatRequest, req: Request):
    rag = req.app.state.pipelines.get(request.repository_id)
    
    question = request.question.strip()
    if not rag:
        raise HTTPException(status_code=400, detail="Question cannot be empty")
        
    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    
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