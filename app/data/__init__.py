"""Data package."""
from app.data.corpus import HISTORICAL_CORPUS, ingest_corpus
from app.data.events import PREDEFINED_EVENTS

__all__ = ["HISTORICAL_CORPUS", "ingest_corpus", "PREDEFINED_EVENTS"]
