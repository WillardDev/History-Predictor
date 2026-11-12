"""Small, dependency-free historical corpus used for lightweight RAG."""
from __future__ import annotations

from typing import Any

from app.core.logger import get_logger

logger = get_logger(__name__)

# Each document is plain text plus a little metadata. Keeping this in memory
# avoids running a vector database just to add a few paragraphs of context.
HISTORICAL_CORPUS: list[dict[str, Any]] = [
    {
        "id": "wwii-end-europe",
        "text": "Germany surrendered unconditionally in May 1945. Europe was divided into occupation zones, millions of people were displaced, and the United States and Soviet Union emerged as rival superpowers.",
        "metadata": {"event_type": "war", "region": "Europe"},
    },
    {
        "id": "marshall-plan",
        "text": "The Marshall Plan sent about 13 billion dollars of American aid to rebuild Western Europe after World War II. It stabilised economies, encouraged cooperation, and deepened the division of Europe.",
        "metadata": {"event_type": "economic_crisis", "region": "Europe"},
    },
    {
        "id": "cold-war-alliances",
        "text": "NATO was founded in 1949 and the Warsaw Pact in 1955. The alliance systems divided Europe, drove arms racing, and made local conflicts potential superpower confrontations.",
        "metadata": {"event_type": "political_crisis", "region": "Global"},
    },
    {
        "id": "decolonisation",
        "text": "After 1945, European empires lost legitimacy and colonies in Asia and Africa gained independence. New states often inherited arbitrary borders, weak institutions, and Cold War competition.",
        "metadata": {"event_type": "political_revolution", "region": "Global"},
    },
    {
        "id": "cuban-missile-crisis",
        "text": "During the Cuban Missile Crisis, the United States and Soviet Union came close to nuclear war. A naval quarantine, secret negotiations, and a public withdrawal of missiles produced a compromise and a hotline.",
        "metadata": {"event_type": "political_crisis", "region": "Caribbean"},
    },
    {
        "id": "berlin-wall",
        "text": "The Berlin Wall fell in November 1989 after mass protests and the opening of border crossings. German reunification followed in 1990, and communist governments across Eastern Europe collapsed.",
        "metadata": {"event_type": "political_revolution", "region": "Europe"},
    },
    {
        "id": "soviet-collapse",
        "text": "The Soviet Union dissolved in 1991 after economic stagnation, nationalist movements, and failed reforms. Russia inherited most of its military power while former republics became independent states.",
        "metadata": {"event_type": "political_revolution", "region": "Eurasia"},
    },
    {
        "id": "wwi-outbreak",
        "text": "The assassination of Archduke Franz Ferdinand in Sarajevo triggered alliance commitments that turned a regional dispute into World War I. Trench warfare and industrial mobilisation produced unprecedented casualties.",
        "metadata": {"event_type": "political_assassination", "region": "Europe"},
    },
    {
        "id": "treaty-of-versailles",
        "text": "The Treaty of Versailles imposed reparations and territorial losses on Germany. Many Germans resented the settlement, and its enforcement shaped interwar politics and the rise of extremist movements.",
        "metadata": {"event_type": "war", "region": "Europe"},
    },
    {
        "id": "black-death",
        "text": "The Black Death killed roughly a third to a half of Europe's population in the mid-fourteenth century. Labour shortages raised wages, weakened serfdom, and shook confidence in traditional authorities.",
        "metadata": {"event_type": "pandemic", "region": "Europe"},
    },
    {
        "id": "industrial-revolution",
        "text": "Industrialisation shifted populations from farms to cities, expanded factory work, and created new social classes. Governments gradually responded with public health measures, unions, and welfare policies.",
        "metadata": {"event_type": "economic_crisis", "region": "Global"},
    },
    {
        "id": "great-depression",
        "text": "The Great Depression began with the 1929 stock market crash and spread through banking failures, protectionism, and mass unemployment. Governments adopted tariffs, public works, and new financial regulations.",
        "metadata": {"event_type": "economic_crisis", "region": "Global"},
    },
    {
        "id": "french-revolution",
        "text": "The French Revolution overthrew the monarchy, reorganised society around citizenship, and produced years of war and political instability. Its ideas about rights and sovereignty spread across Europe.",
        "metadata": {"event_type": "political_revolution", "region": "Europe"},
    },
    {
        "id": "meiji-restoration",
        "text": "Japan's Meiji Restoration rapidly industrialised the country and centralised political power. It created a modern army and navy, expanded education, and set Japan on an imperial path.",
        "metadata": {"event_type": "political_revolution", "region": "Asia"},
    },
    {
        "id": "fall-of-rome",
        "text": "The Western Roman Empire fragmented under military pressure, fiscal strain, and political instability. Local rulers and new kingdoms replaced central authority while Roman law and culture survived in altered forms.",
        "metadata": {"event_type": "general", "region": "Europe"},
    },
]


def ingest_corpus() -> int:
    """Load the in-memory corpus and return the document count."""
    logger.info("Loaded %d historical documents", len(HISTORICAL_CORPUS))
    return len(HISTORICAL_CORPUS)
