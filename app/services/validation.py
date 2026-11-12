"""Basic sanity checks for generated timelines."""
from __future__ import annotations

from typing import Any

from app.models.timeline import AlternateTimelineResponse


class ValidationEngine:
    """Check that a timeline is internally consistent enough to display."""

    def validate(self, timeline: AlternateTimelineResponse) -> dict[str, Any]:
        issues: list[str] = []

        if not timeline.timeline:
            issues.append("Timeline contains no years.")

        years = [entry.year for entry in timeline.timeline]
        if years != sorted(years):
            issues.append("Timeline years are not in ascending order.")
        if len(years) != len(set(years)):
            issues.append("Timeline contains duplicate years.")

        if not 0 <= timeline.plausibility_score <= 10:
            issues.append("Plausibility score must be between 0 and 10.")

        for entry in timeline.timeline:
            for pillar_name in ("social", "economy", "political"):
                pillar = getattr(entry, pillar_name)
                for field, value in pillar.model_dump().items():
                    if not str(value).strip():
                        issues.append(f"Year {entry.year}: {pillar_name}.{field} is empty.")

        return {
            "valid": not issues,
            "issues": issues,
            "year_count": len(timeline.timeline),
        }


validation_engine = ValidationEngine()
