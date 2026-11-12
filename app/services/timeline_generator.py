"""Enhanced timeline generator with RAG integration and caching."""
from __future__ import annotations

import hashlib
import json
from collections.abc import AsyncIterator

from app.core.llm_client import llm_client
from app.core.logger import get_logger
from app.data.corpus import ingest_corpus
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
from app.services.rag_pipeline import rag_pipeline
from app.services.cache import cache_manager

logger = get_logger(__name__)


class TimelineGenerator:
    """Generates alternate timelines using LLM with RAG integration."""

    def __init__(self) -> None:
        self.llm = llm_client
        # Ingest corpus on startup
        ingest_corpus()

    async def generate(
        self,
        event: HistoricalEvent,
        num_years: int = 6,
        focus_pillars: list[str] | None = None,
        additional_context: str | None = None,
        use_rag: bool = True,
    ) -> AlternateTimelineResponse:
        """Generate an alternate timeline for a historical event."""
        # Build RAG context
        rag_context = ""
        if use_rag:
            query = f"{event.name} {event.event_type} {event.geographic_scope}"
            rag_context = rag_pipeline.build_context(
                query=query,
                n_results=3,
                event_type=event.event_type,
            )

        # Combine contexts
        full_context = additional_context or ""
        if rag_context:
            if full_context:
                full_context = f"{full_context}\n\nHISTORICAL CONTEXT:\n{rag_context}"
            else:
                full_context = f"HISTORICAL CONTEXT:\n{rag_context}"

        user_prompt = build_user_prompt(
            event=event,
            num_years=num_years,
            focus_pillars=focus_pillars,
            additional_context=full_context,
        )

        # Check cache
        cache_key = self._make_cache_key(
            event=event,
            num_years=num_years,
            focus_pillars=focus_pillars,
            context_hash=hashlib.md5(full_context.encode()).hexdigest(),
        )

        cached = await cache_manager.get(cache_key)
        if cached:
            logger.info(f"Cache hit for {event.name}")
            return parse_timeline_response(cached)

        logger.info(
            f"Generating timeline for event: {event.name} "
            f"({num_years} years, pillars: {focus_pillars or 'all'})"
        )

        try:
            raw_response = await self.llm.generate_json(
                prompt=user_prompt,
                system_prompt=SYSTEM_PROMPT,
                schema=get_output_schema(),
            )

            timeline = parse_timeline_response(raw_response)

            # Cache the result
            await cache_manager.set(
                cache_key,
                timeline.model_dump(),
                ttl=7200,  # 2 hours
            )

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
        num_years: int = 6,
        focus_pillars: list[str] | None = None,
        additional_context: str | None = None,
    ) -> AsyncIterator[str]:
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

    def _make_cache_key(
        self,
        event: HistoricalEvent,
        num_years: int,
        focus_pillars: list[str] | None,
        context_hash: str,
    ) -> str:
        """Create a cache key for a generation request."""
        key_data = {
            "event_name": event.name,
            "num_years": num_years,
            "focus_pillars": focus_pillars or [],
            "context_hash": context_hash,
        }
        return json.dumps(key_data, sort_keys=True)


# Singleton instance
timeline_generator = TimelineGenerator()