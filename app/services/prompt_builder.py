"""Prompt template construction and management."""
from __future__ import annotations

import json
from typing import Any

from app.models.timeline import AlternateTimelineResponse, HistoricalEvent


SYSTEM_PROMPT = """
You are a counterfactual historian. Generate plausible alternate timelines as valid JSON.

CRITICAL: Return ONLY valid JSON. No markdown, no explanation, no code blocks.

RULES:
1. Changes must be historically plausible for the era (no sci-fi/fantasy)
2. Each year must logically follow from the previous
3. Consider ripple effects across social, economic, and political spheres
4. Keep each field concise (1-3 sentences)

OUTPUT JSON:
{
  "pivot": {"event": "...", "date": "...", "divergence_point": "...", "immediate_causes": "..."},
  "timeline": [{"year": 1946, "social": {"culture": "...", "daily_life": "...", "demographics": "...", "public_sentiment": "..."}, "economy": {"trade_routes": "...", "currency_stability": "...", "labor_markets": "...", "industrial_impacts": "..."}, "political": {"governance": "...", "treaties": "...", "alliances": "...", "power_dynamics": "..."}}],
  "long_term_consequences": {"global_order": "...", "technological_divergence": "...", "cultural_legacy": "...", "lessons_learned": "..."},
  "plausibility_score": 7.5,
  "historical_grounding": "...",
  "confidence_level": "High"
}
"""


def build_user_prompt(
    event: HistoricalEvent,
    num_years: int = 20,
    focus_pillars: list[str] | None = None,
    additional_context: str | None = None,
) -> str:
    """Build the user prompt for an alternate timeline simulation.

    Args:
        event: The historical event to simulate.
        num_years: Number of years to project forward.
        focus_pillars: Optional pillars to emphasize.
        additional_context: Extra context from RAG or user input.

    Returns:
        Formatted user prompt.
    """
    pillars_desc = (
        ", ".join(focus_pillars)
        if focus_pillars
        else "social, economic, and political"
    )

    prompt = f"""Generate an alternate timeline for the following historical event:

EVENT: {event.name}
TIME PERIOD: {event.start_date} to {event.end_date or 'ongoing'}
TYPE: {event.event_type}
GEOGRAPHIC SCOPE: {event.geographic_scope}
DESCRIPTION: {event.description}
"""

    if event.key_figures:
        prompt += f"KEY FIGURES: {', '.join(event.key_figures)}\n"

    prompt += f"""
INSTRUCTIONS:
- Project the alternate timeline for {num_years} years after the pivot point.
- Focus on these pillars in detail: {pillars_desc}.
- Each year should have distinct, meaningful changes across all three pillars.
- Ensure causal consistency: each year's changes should logically follow from previous years.
- Ground all claims in historical plausibility for the era.

"""

    if additional_context:
        prompt += f"HISTORICAL CONTEXT (use this to ground your analysis):\n{additional_context}\n\n"

    prompt += "Respond with a JSON object following the specified structure."

    return prompt


def get_output_schema() -> dict[str, Any]:
    """Get the JSON schema for the alternate timeline response."""
    return AlternateTimelineResponse.model_json_schema()


def parse_timeline_response(raw_response: str | dict) -> AlternateTimelineResponse:
    """Parse and validate an LLM response into the structured timeline model.

    Args:
        raw_response: Raw JSON string or dict from the LLM.

    Returns:
        Validated AlternateTimelineResponse.

    Raises:
        ValueError: If the response cannot be parsed.
    """
    if isinstance(raw_response, dict):
        data = raw_response
    else:
        data = json.loads(raw_response)
    return AlternateTimelineResponse.model_validate(data)