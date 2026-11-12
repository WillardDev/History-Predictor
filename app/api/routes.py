"""FastAPI routes for timeline generation."""
from __future__ import annotations

import time

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import StreamingResponse

from app.api.schemas import (
    GenerateRequest,
    GenerateResponse,
    GenerateStreamRequest,
    HealthResponse,
)
from app.core.config import settings
from app.core.logger import get_logger
from app.services.timeline_generator import timeline_generator
from app.services.rag_pipeline import rag_pipeline
from app.services.validation import validation_engine

logger = get_logger(__name__)

router = APIRouter(prefix="/api/v1", tags=["timeline"])


def _friendly_error(error: Exception) -> HTTPException:
    """Turn provider errors into short messages the website can display."""
    message = str(error)
    if "rate_limit" in message or "429" in message:
        return HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="The AI service is busy right now. Please wait a minute and try again.",
        )
    if "json_validate" in message or "Failed to generate JSON" in message:
        return HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="The AI returned an invalid timeline. Please try again.",
        )
    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Timeline generation failed. Please try again.",
    )


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Check API health and model status."""
    return HealthResponse(
        status="healthy",
        version=settings.app_version,
        model=settings.groq_model,
    )


@router.post("/generate", response_model=GenerateResponse)
async def generate_timeline(
    request: GenerateRequest,
) -> GenerateResponse:
    """Generate an alternate timeline for a historical event.

    This is the primary endpoint. It processes the event, builds a prompt,
    calls the LLM, and returns a structured alternate timeline with the
    three pillars (social, economy, political) for each year.
    """
    start_time = time.time()

    try:
        timeline = await timeline_generator.generate(
            event=request.event,
            num_years=request.num_years,
            focus_pillars=request.focus_pillars,
            additional_context=request.additional_context,
            use_rag=True,
        )

        # Validate the timeline
        validation = validation_engine.validate(timeline)

        processing_time = (time.time() - start_time) * 1000

        return GenerateResponse(
            success=True,
            data=timeline,
            validation=validation,
            processing_time_ms=processing_time,
        )
    except Exception as e:
        logger.error(f"Generation failed: {e}")
        raise _friendly_error(e)


@router.post("/generate/stream")
async def generate_timeline_stream(
    request: GenerateStreamRequest,
):
    """Stream a timeline generation as raw text chunks (SSE)."""
    try:
        async def event_generator():
            async for chunk in timeline_generator.generate_stream(
                event=request.event,
                num_years=request.num_years,
                focus_pillars=request.focus_pillars,
                additional_context=request.additional_context,
            ):
                yield f"data: {chunk}\n\n"

        return StreamingResponse(
            event_generator(),
            media_type="text/event-stream",
        )
    except Exception as e:
        logger.error(f"Streaming failed: {e}")
        raise _friendly_error(e)


@router.get("/events")
async def list_predefined_events() -> dict:
    """List predefined historical events available for simulation."""
    from app.data.events import PREDEFINED_EVENTS

    return {
        "events": [e.model_dump() for e in PREDEFINED_EVENTS.values()],
        "count": len(PREDEFINED_EVENTS),
    }


@router.post("/corpus/reset")
async def reset_corpus() -> dict:
    """Reset the RAG corpus."""
    from app.data.corpus import ingest_corpus

    ingest_corpus()
    return {"status": "ok", "message": "Corpus reset successfully"}


@router.get("/corpus/search")
async def search_corpus(
    query: str,
    n_results: int = 5,
) -> dict:
    """Search the historical corpus for relevant context."""
    results = rag_pipeline.retrieve(query=query, n_results=n_results)
    return {
        "query": query,
        "results": results,
        "count": len(results),
    }