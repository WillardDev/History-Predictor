"""Very small keyword-based retrieval layer.

This is deliberately not a vector database. The corpus is tiny, so matching
shared words is fast, predictable, and needs no model downloads.
"""
from __future__ import annotations

import re
from typing import Any

from app.data.corpus import HISTORICAL_CORPUS

STOPWORDS = {
    "the", "and", "for", "with", "that", "this", "from", "into", "after",
    "before", "during", "over", "under", "about", "were", "was", "are",
    "its", "their", "they", "have", "has", "had", "not", "but", "which",
    "what", "when", "where", "who", "how", "all", "any", "can", "may",
}


def _tokens(text: str) -> set[str]:
    words = re.findall(r"[a-z0-9]+", text.lower())
    return {word for word in words if len(word) > 2 and word not in STOPWORDS}


class RAGPipeline:
    """Retrieve the most relevant corpus paragraphs for a query."""

    def retrieve(
        self,
        query: str,
        n_results: int = 5,
        event_type: str | None = None,
    ) -> list[dict[str, Any]]:
        query_tokens = _tokens(query)
        if not query_tokens:
            return []

        scored: list[dict[str, Any]] = []
        for document in HISTORICAL_CORPUS:
            score = len(query_tokens & _tokens(document["text"]))
            metadata = document.get("metadata", {})
            if event_type and metadata.get("event_type") == event_type:
                score += 3
            if score <= 0:
                continue
            scored.append(
                {
                    "id": document["id"],
                    "text": document["text"],
                    "metadata": metadata,
                    "score": score,
                }
            )

        scored.sort(key=lambda item: item["score"], reverse=True)
        return scored[:n_results]

    def build_context(
        self,
        query: str,
        n_results: int = 3,
        event_type: str | None = None,
    ) -> str:
        """Return retrieved documents as a short bullet list."""
        results = self.retrieve(
            query=query,
            n_results=n_results,
            event_type=event_type,
        )
        if not results:
            return ""
        return "\n".join(f"- {result['text']}" for result in results)


rag_pipeline = RAGPipeline()
