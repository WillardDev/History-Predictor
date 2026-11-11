# History Predictor

Simulates and predicts detailed alternate endings for major historical events.

## Quick Start

```bash
pip install -e .
cp .env.example .env
# Edit .env with your API keys
uvicorn app.main:app --reload
```

## Architecture

See the technical guide for full details. This is a FastAPI backend with:
- RAG pipeline (Chroma/Pinecone)
- LLM orchestration (LangChain/LlamaIndex)
- Structured output (Pydantic models)
- Async task processing (Celery)