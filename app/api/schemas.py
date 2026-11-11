"""Pydantic schemas for API requests and responses."""
from __future__ import annotations

from pydantic import BaseModel, Field

from app.models.timeline import (
    AlternateTimelineResponse,
    HistoricalEvent,
    LongTermConsequences,
    SocialPillar,
    EconomyPillar,
    PoliticalPillar,
    TimelineEntry,
)


# Request schemas
class GenerateRequest(BaseModel):
    """Request to generate an alternate timeline."""

    event: HistoricalEvent = Field(..., description="The historical event to simulate")
    num_years: int = Field(default=20, ge=1, le=50, description="Years to project forward")
    focus_pillars: list[str] | None = Field(
        default=None,
        description="Pillars to emphasize: social, economy, political",
    )
    additional_context: str | None = Field(
        default=None,
        description="Extra context to ground the simulation",
    )


class GenerateStreamRequest(BaseModel):
    """Request to stream a timeline generation."""

    event: HistoricalEvent = Field(..., description="The historical event to simulate")
    num_years: int = Field(default=20, ge=1, le=50, description="Years to project forward")
    focus_pillars: list[str] | None = Field(default=None)
    additional_context: str | None = Field(default=None)


# Response schemas
class HealthResponse(BaseModel):
    """Health check response."""

    status: str = Field(default="healthy")
    version: str = Field(default="0.1.0")
    model: str | None = Field(default=None)


class GenerateResponse(BaseModel):
    """Response wrapper for timeline generation."""

    success: bool = Field(default=True)
    data: AlternateTimelineResponse
    processing_time_ms: float | None = Field(default=None)


class EventListResponse(BaseModel):
    """Response for listing predefined events."""

    events: list[HistoricalEvent]
    count: int