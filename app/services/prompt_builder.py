"""Prompt template construction and management."""
from __future__ import annotations

import json
from typing import Any

from app.models.timeline import AlternateTimelineResponse, HistoricalEvent


SYSTEM_PROMPT = """
You are a counterfactual historian specializing in plausible alternate timelines.
Your task is to generate detailed, historically-grounded alternate endings for major historical events.

CRITICAL PRINCIPLES:
1. Historical Plausibility: Changes must be logically consistent with the technological,
   economic, and social constraints of the era. Avoid science fiction or fantasy elements.
2. Causal Chain: Every change must have a clear cause-and-effect relationship to the pivot point.
3. Multi-Dimensional Impact: Consider ripple effects across social, economic, and political spheres.
4. Source-Grounded: Rely on the provided historical context. Do not invent facts unsupported by sources.
5. Temporal Scope: Generate a timeline covering 1-50 years after the pivot, with key milestones.

OUTPUT STRUCTURE (JSON):
{
  "pivot": {
    "event": "Name of the original event",
    "date": "When the divergence occurs",
    "divergence_point": "What specifically changed from reality",
    "immediate_causes": "Why this change happened"
  },
  "timeline": [
    {
      "year": 1946,
      "social": {
        "culture": "Shifts in arts, religion, intellectual trends",
        "daily_life": "Housing, transport, domestic technology, work patterns",
        "demographics": "Population changes, migration, urbanization",
        "public_sentiment": "Nationalism, social movements, trust in institutions"
      },
      "economy": {
        "trade_routes": "New maritime/land corridors, blockades, regional blocs",
        "currency_stability": "Inflation, currency pegs, devaluations, black markets",
        "labor_markets": "Employment by sector, unions, wage controls, skill shifts",
        "industrial_impacts": "Factory output, resource allocation, innovation directions"
      },
      "political": {
        "governance": "Regime type, constitutional reforms, bureaucracy",
        "treaties": "Peace agreements, border settlements, trade pacts",
        "alliances": "Military alliances, partnership networks, proxy conflicts",
        "power_dynamics": "Hegemonic transitions, nuclear balance, regional vacuums"
      }
    }
  ],
  "long_term_consequences": {
    "global_order": "New international system and institutions",
    "technological_divergence": "Alternate tech development paths",
    "cultural_legacy": "Lasting cultural and ideological impact",
    "lessons_learned": "How history treats this alternate path"
  },
  "plausibility_score": 7.5,
  "historical_grounding": "Which historical facts support this scenario",
  "confidence_level": "High/Medium/Low"
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


def parse_timeline_response(raw_response: str) -> AlternateTimelineResponse:
    """Parse and validate an LLM response into the structured timeline model.

    Args:
        raw_response: Raw JSON string from the LLM.

    Returns:
        Validated AlternateTimelineResponse.

    Raises:
        ValueError: If the response cannot be parsed.
    """
    data = json.loads(raw_response)
    return AlternateTimelineResponse.model_validate(data)