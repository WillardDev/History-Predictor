"""Predefined historical events for quick simulation."""
from __future__ import annotations

from app.models.timeline import HistoricalEvent


PREDEFINED_EVENTS: dict[str, HistoricalEvent] = {
    "wwii_1945": HistoricalEvent(
        name="End of World War II in Europe",
        start_date="1945-04-30",
        end_date="1945-05-08",
        description="The surrender of Nazi Germany and the end of WWII in Europe. "
        "This event reshaped global politics, led to the Cold War, and set the stage "
        "for decolonization and international institutions.",
        key_figures=["Adolf Hitler", "Winston Churchill", "Joseph Stalin", "Dwight Eisenhower"],
        geographic_scope="Europe",
        event_type="war",
    ),
    "cuban_missile_crisis": HistoricalEvent(
        name="Cuban Missile Crisis",
        start_date="1962-10-16",
        end_date="1962-10-28",
        description="A 35-day confrontation between the United States and the Soviet Union "
        "over Soviet ballistic missiles deployed in Cuba. It was the closest the Cold War "
        "came to nuclear conflict.",
        key_figures=["John F. Kennedy", "Nikita Khrushchev", "Fidel Castro"],
        geographic_scope="Caribbean / Global",
        event_type="political_crisis",
    ),
    "fall_of_berlin_wall": HistoricalEvent(
        name="Fall of the Berlin Wall",
        start_date="1989-11-09",
        end_date="1990-10-03",
        description="The opening of the Berlin Wall and the subsequent reunification of Germany. "
        "This symbolized the end of the Cold War and the collapse of communist regimes in Eastern Europe.",
        key_figures=["Mikhail Gorbachev", "Helmut Kohl", "Erich Honecker"],
        geographic_scope="Germany / Eastern Europe",
        event_type="political_revolution",
    ),
    "assassination_of_archduke": HistoricalEvent(
        name="Assassination of Archduke Franz Ferdinand",
        start_date="1914-06-28",
        end_date="1914-08-01",
        description="The assassination of Archduke Franz Ferdinand of Austria in Sarajevo "
        "triggered a chain of events that led to World War I.",
        key_figures=["Gavrilo Princip", "Franz Ferdinand", "Kaiser Wilhelm"],
        geographic_scope="Europe",
        event_type="political_assassination",
    ),
    "black_death": HistoricalEvent(
        name="The Black Death",
        start_date="1347",
        end_date="1351",
        description="A bubonic plague pandemic that ravaged Europe, killing 30-60% of the population. "
        "It fundamentally transformed European society, economy, and religion.",
        key_figures=[],
        geographic_scope="Europe / Asia",
        event_type="pandemic",
    ),
}