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
4. Keep every field to a short phrase (maximum 8 words)
5. Return exactly the requested number of timeline entries

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
    num_years: int = 6,
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
- Return exactly {num_years} timeline entries, one for each year.
- Focus on these pillars in detail: {pillars_desc}.
- Each year should have distinct, meaningful changes across all three pillars.
- Ensure causal consistency: each year's changes should logically follow from previous years.
- Ground all claims in historical plausibility for the era.
- Keep each field to a short phrase (maximum 8 words).

"""

    if additional_context:
        prompt += f"HISTORICAL CONTEXT (use this to ground your analysis):\n{additional_context}\n\n"

    prompt += "Respond with a JSON object following the specified structure."

    return prompt


def get_output_schema() -> dict[str, Any]:
    """Compact JSON schema used for Groq structured output."""

    def string(description: str) -> dict[str, str]:
        return {"type": "string", "description": description}

    def obj(properties: dict[str, dict[str, Any]]) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": properties,
            "required": list(properties),
            "additionalProperties": False,
        }

    social = obj(
        {
            "culture": string("Culture, arts, and intellectual trends"),
            "daily_life": string("Daily life, housing, and domestic technology"),
            "demographics": string("Population, migration, and urbanisation"),
            "public_sentiment": string("Public opinion and social movements"),
        }
    )
    economy = obj(
        {
            "trade_routes": string("Trade routes and regional trade blocs"),
            "currency_stability": string("Inflation, currency pegs, black markets"),
            "labor_markets": string("Employment, unions, and wages"),
            "industrial_impacts": string("Factory output, resources, and innovation"),
        }
    )
    political = obj(
        {
            "governance": string("Regime type, reforms, and bureaucracy"),
            "treaties": string("Peace agreements and trade pacts"),
            "alliances": string("Military alliances and proxy conflicts"),
            "power_dynamics": string("Hegemonic transitions and regional vacuums"),
        }
    )

    return {
        "type": "object",
        "properties": {
            "pivot": obj(
                {
                    "event": string("The event that diverges"),
                    "date": string("Date of the divergence"),
                    "divergence_point": string("What changed and why"),
                    "immediate_causes": string("Immediate causes of the change"),
                }
            ),
            "timeline": {
                "type": "array",
                "items": obj(
                    {
                        "year": {"type": "integer", "description": "Year of this entry"},
                        "social": social,
                        "economy": economy,
                        "political": political,
                    }
                ),
            },
            "long_term_consequences": obj(
                {
                    "global_order": string("New global order"),
                    "technological_divergence": string("Alternate technology path"),
                    "cultural_legacy": string("Lasting cultural impact"),
                    "lessons_learned": string("How history treats this path"),
                }
            ),
            "plausibility_score": {
                "type": "number",
                "description": "Self-assessed plausibility from 0 to 10",
            },
            "historical_grounding": string("Historical basis for the scenario"),
            "confidence_level": {
                "type": "string",
                "enum": ["High", "Medium", "Low"],
            },
        },
        "required": [
            "pivot",
            "timeline",
            "long_term_consequences",
            "plausibility_score",
            "historical_grounding",
            "confidence_level",
        ],
        "additionalProperties": False,
    }


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