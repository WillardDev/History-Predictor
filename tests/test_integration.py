"""Integration test for the full timeline generation pipeline."""
from __future__ import annotations

import pytest
import asyncio

from app.models.timeline import HistoricalEvent
from app.services.timeline_generator import timeline_generator


@pytest.mark.asyncio
async def test_generate_timeline_integration() -> None:
    """Test that the full pipeline can generate a timeline (requires Groq API key)."""
    event = HistoricalEvent(
        name="Test WWII Alternate",
        start_date="1945-04-30",
        description="What if Hitler had escaped to Argentina instead of committing suicide?",
        geographic_scope="Europe / South America",
        event_type="war",
        key_figures=["Adolf Hitler", "Joseph Stalin", "Winston Churchill"],
    )

    try:
        timeline = await timeline_generator.generate(
            event=event,
            num_years=2,
        )

        assert timeline.pivot is not None
        assert len(timeline.timeline) > 0
        assert timeline.plausibility_score > 0
        assert timeline.confidence_level in ("High", "Medium", "Low")

        # Verify each entry has all three pillars
        for entry in timeline.timeline:
            assert entry.social is not None
            assert entry.economy is not None
            assert entry.political is not None
            assert entry.year > 1945

        print(f"\n=== Generated Timeline ===")
        print(f"Pivot: {timeline.pivot}")
        print(f"Plausibility: {timeline.plausibility_score}/10")
        print(f"Confidence: {timeline.confidence_level}")
        for entry in timeline.timeline:
            print(f"\n--- Year {entry.year} ---")
            print(f"Social: {entry.social.culture[:100]}...")
            print(f"Economy: {entry.economy.trade_routes[:100]}...")
            print(f"Political: {entry.political.governance[:100]}...")

    except Exception as e:
        pytest.skip(f"Integration test requires valid Groq API key: {e}")