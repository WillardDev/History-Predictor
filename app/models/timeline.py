"""Pydantic models for events, timelines, and the three pillars."""
from __future__ import annotations

from pydantic import BaseModel, Field
from typing import Any


# ---------------------------------------------------------------------------
# Core domain models
# ---------------------------------------------------------------------------


class HistoricalEvent(BaseModel):
    """A historical event to simulate an alternate ending for."""

    name: str = Field(..., description="Name of the historical event")
    start_date: str = Field(..., description="Start date (YYYY or YYYY-MM-DD)")
    end_date: str | None = Field(default=None, description="End date if applicable")
    description: str = Field(..., description="Brief description of the event")
    key_figures: list[str] = Field(
        default_factory=list,
        description="Key historical figures involved",
    )
    geographic_scope: str = Field(..., description="Primary geographic region")
    event_type: str = Field(
        default="general",
        description="Type: war, political_revolution, economic_crisis, etc.",
    )


class SocialPillar(BaseModel):
    """Social settings in an alternate timeline."""

    culture: str = Field(..., description="Shifts in culture, arts, and intellectual trends")
    daily_life: str = Field(..., description="Changes in daily life, housing, and domestic technology")
    demographics: str = Field(..., description="Population changes, migration, urbanization")
    public_sentiment: str = Field(..., description="Public opinion, social movements, trust in institutions")


class EconomyPillar(BaseModel):
    """Economy settings in an alternate timeline."""

    trade_routes: str = Field(..., description="Changes in trade routes and regional trade blocs")
    currency_stability: str = Field(..., description="Inflation, currency pegs, black market rates")
    labor_markets: str = Field(..., description="Employment, unions, wage controls, skill shifts")
    industrial_impacts: str = Field(..., description="Factory output, resource allocation, innovation")


class PoliticalPillar(BaseModel):
    """Political settings in an alternate timeline."""

    governance: str = Field(..., description="Regime type, constitutional reforms, bureaucracy")
    treaties: str = Field(..., description="Peace agreements, border settlements, trade pacts")
    alliances: str = Field(..., description="Military alliances, partnership networks, proxy conflicts")
    power_dynamics: str = Field(..., description="Hegemonic transitions, nuclear balance, regional vacuums")


class TimelineEntry(BaseModel):
    """A single year's entry in an alternate timeline."""

    year: int = Field(..., description="Year relative to the pivot point")
    social: SocialPillar = Field(..., description="Social settings for this year")
    economy: EconomyPillar = Field(..., description="Economy settings for this year")
    political: PoliticalPillar = Field(..., description="Political settings for this year")


class LongTermConsequences(BaseModel):
    """Long-term consequences of the alternate ending."""

    global_order: str = Field(..., description="New global order and international system")
    technological_divergence: str = Field(..., description="Alternate technological development paths")
    cultural_legacy: str = Field(..., description="Lasting cultural and ideological impact")
    lessons_learned: str = Field(..., description="How history treats this alternate path")


class AlternateTimelineResponse(BaseModel):
    """Complete response for an alternate timeline simulation."""

    pivot: dict[str, Any] = Field(..., description="The pivot point and divergence details")
    timeline: list[TimelineEntry] = Field(..., description="Year-by-year alternate timeline")
    long_term_consequences: LongTermConsequences = Field(..., description="Long-term global impact")
    plausibility_score: float = Field(..., description="Self-assessed plausibility (0-10)")
    historical_grounding: str = Field(..., description="Which sources support this scenario")
    confidence_level: str = Field(..., description="High/Medium/Low confidence in this scenario")