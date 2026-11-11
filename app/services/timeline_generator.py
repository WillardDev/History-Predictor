"""Core timeline generation service."""
from __future__ import annotations

import json
import logging
from typing import Any

from app.core.config import settings
from app.core.llm_client import llm_client
from app.core.logger import get_logger
from app.models.timeline import (
    AlternateTimelineResponse,
    HistoricalEvent,
)
from app.services.prompt_builder import (
    SYSTEM_PROMPT,
    build_user_prompt,
    get_output_schema,
    parse_timeline_response,
)

logger = get_logger(__name__)


class TimelineGenerator:
    """Generates alternate timelines using the LLM."""

    def __init__(self) -> None:
        self.llm = llm_client

    async def generate(
        self,
        event: HistoricalEvent,
        num_years: int = 20,
        focus_pillars: list[str] | None = None,
        additional_context: str | None = None,
    ) -> AlternateTimelineResponse:
        """Generate an alternate timeline for a historical event.

        Args:
            event: The historical event to simulate.
            num_years: Number of years to project forward.
            focus_pillars: Optional pillars to emphasize.
            additional_context: Extra context from RAG or user input.

        Returns:
            Structured alternate timeline response.
        """
        user_prompt = build_user_prompt(
            event=event,
            num_years=num_years,
            focus_pillars=focus_pillars,
            additional_context=additional_context,
        )
        schema = get_output_schema()

        logger.info(
            f"Generating timeline for event: {event.name} "
            f"({num_years} years, pillars: {focus_pillars or 'all'})"
        )

        try:
            raw_response = await self.llm.generate_json(
                prompt=user_prompt,
                system_prompt=SYSTEM_PROMPT,
                schema=schema,
            )

            timeline = parse_timeline_response(raw_response)

            logger.info(
                f"Successfully generated timeline for {event.name} "
                f"(plausibility: {timeline.plausibility_score}/10)"
            )

            return timeline
        except Exception as e:
            logger.error(f"Failed to generate timeline for {event.name}: {e}")
            raise

    async def generate_stream(
        self,
        event: HistoricalEvent,
        num_years: int = 20,
        focus_pillars: list[str] | None = None,
        additional_context: str | None = None,
    ) -> Any:
        """Stream a timeline generation (yields raw text chunks)."""
        user_prompt = build_user_prompt(
            event=event,
            num_years=num_years,
            focus_pillars=focus_pillars,
            additional_context=additional_context,
        )

        async for chunk in self.llm.stream(
            prompt=user_prompt,
            system_prompt=SYSTEM_PROMPT,
        ):
            yield chunk


# Singleton instance
timeline_generator = TimelineGenerator()