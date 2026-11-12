"""History Predictor - FastAPI application entry point."""
from __future__ import annotations

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.api.routes import router
from app.core.config import settings
from app.core.logger import setup_logging

STATIC_DIR = Path(__file__).parent / "static"

# Setup logging on startup
setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown tasks."""
    print(f"\n{'='*60}")
    print(f"  {settings.app_name} v{settings.app_version}")
    print(f"  LLM: {settings.groq_model}")
    print(f"  Docs: http://localhost:8000/docs")
    print(f"{'='*60}\n")
    yield


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Simulates and predicts detailed alternate endings for major historical events.",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router)

# Serve the website
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/", include_in_schema=False)
async def root() -> FileResponse:
    """Serve the History Predictor website."""
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/api", include_in_schema=False)
async def api_info() -> dict:
    """Small machine-readable entry point for API clients."""
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "docs": "/docs",
        "health": "/api/v1/health",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level="info",
    )