"""Tests for the History Predictor application."""
from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.models.timeline import (
    AlternateTimelineResponse,
    HistoricalEvent,
    SocialPillar,
    EconomyPillar,
    PoliticalPillar,
    TimelineEntry,
    LongTermConsequences,
)


@pytest.fixture
def client() -> TestClient:
    """Create a test client."""
    return TestClient(app)


@pytest.fixture
def sample_event() -> HistoricalEvent:
    """A sample historical event for testing."""
    return HistoricalEvent(
        name="Test Event",
        start_date="1945-01-01",
        description="A test historical event",
        geographic_scope="Europe",
        event_type="war",
    )


class TestHealth:
    """Tests for the health endpoint."""

    def test_health_check(self, client: TestClient) -> None:
        """Test that health endpoint returns healthy status."""
        response = client.get("/api/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["version"] == "0.1.0"


class TestModels:
    """Tests for Pydantic models."""

    def test_social_pillar_validation(self) -> None:
        """Test that SocialPillar validates correctly."""
        pillar = SocialPillar(
            culture="Test culture",
            daily_life="Test daily life",
            demographics="Test demographics",
            public_sentiment="Test sentiment",
        )
        assert pillar.culture == "Test culture"

    def test_timeline_entry_validation(self) -> None:
        """Test that TimelineEntry validates correctly."""
        entry = TimelineEntry(
            year=1946,
            social=SocialPillar(
                culture="Test",
                daily_life="Test",
                demographics="Test",
                public_sentiment="Test",
            ),
            economy=EconomyPillar(
                trade_routes="Test",
                currency_stability="Test",
                labor_markets="Test",
                industrial_impacts="Test",
            ),
            political=PoliticalPillar(
                governance="Test",
                treaties="Test",
                alliances="Test",
                power_dynamics="Test",
            ),
        )
        assert entry.year == 1946

    def test_full_response_validation(self) -> None:
        """Test that AlternateTimelineResponse validates correctly."""
        response = AlternateTimelineResponse(
            pivot={
                "event": "Test Event",
                "date": "1945-01-01",
                "divergence_point": "Test divergence",
                "immediate_causes": "Test causes",
            },
            timeline=[
                TimelineEntry(
                    year=1946,
                    social=SocialPillar(
                        culture="Test",
                        daily_life="Test",
                        demographics="Test",
                        public_sentiment="Test",
                    ),
                    economy=EconomyPillar(
                        trade_routes="Test",
                        currency_stability="Test",
                        labor_markets="Test",
                        industrial_impacts="Test",
                    ),
                    political=PoliticalPillar(
                        governance="Test",
                        treaties="Test",
                        alliances="Test",
                        power_dynamics="Test",
                    ),
                )
            ],
            long_term_consequences=LongTermConsequences(
                global_order="Test",
                technological_divergence="Test",
                cultural_legacy="Test",
                lessons_learned="Test",
            ),
            plausibility_score=7.5,
            historical_grounding="Test",
            confidence_level="High",
        )
        assert response.plausibility_score == 7.5
        assert len(response.timeline) == 1


class TestPromptBuilder:
    """Tests for the prompt builder."""

    def test_build_user_prompt(self, sample_event: HistoricalEvent) -> None:
        """Test that user prompt is built correctly."""
        from app.services.prompt_builder import build_user_prompt

        prompt = build_user_prompt(
            event=sample_event,
            num_years=10,
            focus_pillars=["social", "economy"],
        )
        assert "Test Event" in prompt
        assert "10" in prompt
        assert "social" in prompt
        assert "economy" in prompt

    def test_build_user_prompt_with_context(self, sample_event: HistoricalEvent) -> None:
        """Test that additional context is included."""
        from app.services.prompt_builder import build_user_prompt

        prompt = build_user_prompt(
            event=sample_event,
            num_years=5,
            additional_context="Extra historical context here.",
        )
        assert "Extra historical context here." in prompt