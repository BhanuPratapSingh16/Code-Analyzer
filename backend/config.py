import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")

OLLAMA_MODEL = "qwen3:4b"
OLLAMA_HOST = "http://localhost:11434"

REPOSITORY_ROOT = Path("storage/repositories").resolve()
MAX_UPLOAD_SIZE = 100 * 1024 * 1024
MAX_EXTRACTED_SIZE = 500 * 1024 * 1024
MAX_FILES = 1000
CHUNK_SIZE = 1024 * 1024