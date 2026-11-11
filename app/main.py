"""History Predictor - FastAPI application entry point."""
from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.core.config import settings
from app.core.logger import setup_logging

# Setup logging on startup
setup_logging()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Simulates and predicts detailed alternate endings for major historical events.",
    docs="/docs",
    redoc="/redoc",
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


@app.get("/")
async def root() -> dict:
    """Root endpoint with API info."""
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "docs": "/docs",
        "health": "/api/v1/health",
    }


@app.on_event("startup")
async def startup_event() -> None:
    """Startup tasks."""
    print(f"\n{'='*60}")
    print(f"  {settings.app_name} v{settings.app_version}")
    print(f"  LLM: {settings.groq_model}")
    print(f"  Docs: http://localhost:8000/docs")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level="info",
    )