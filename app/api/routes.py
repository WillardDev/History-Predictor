"""FastAPI routes for timeline generation."""
from __future__ import annotations

import asyncio
import logging
import time
from typing import Annotated

from fastapi import APIRouter, HTTPException, Request, status
from fastapi.responses import StreamingResponse

from app.api.dependencies import APIKey
from app.api.schemas import (
    GenerateRequest,
    GenerateResponse,
    GenerateStreamRequest,
    HealthResponse,
)
from app.core.config import settings
from app.core.logger import get_logger
from app.services.timeline_generator import timeline_generator

logger = get_logger(__name__)

router = APIRouter(prefix="/api/v1", tags=["timeline"])


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
    api_key: Annotated[str, APIKey],
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
        )

        processing_time = (time.time() - start_time) * 1000

        return GenerateResponse(
            success=True,
            data=timeline,
            processing_time_ms=processing_time,
        )
    except Exception as e:
        logger.error(f"Generation failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Timeline generation failed: {str(e)}",
        )


@router.post("/generate/stream")
async def generate_timeline_stream(
    request: GenerateStreamRequest,
    api_key: Annotated[str, APIKey],
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
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Streaming failed: {str(e)}",
        )


@router.get("/events")
async def list_predefined_events(
    api_key: Annotated[str, APIKey],
) -> dict:
    """List predefined historical events available for simulation."""
    from app.data.events import PREDEFINED_EVENTS

    return {
        "events": [e.model_dump() for e in PREDEFINED_EVENTS.values()],
        "count": len(PREDEFINED_EVENTS),
    }