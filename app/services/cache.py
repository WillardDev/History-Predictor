"""Tiny in-process TTL cache.

Good enough for a single-process demo. Swap in Redis if this ever scales.
"""
from __future__ import annotations

import time
from typing import Any


class CacheManager:
    """Store JSON-friendly values in memory with an expiry time."""

    def __init__(self) -> None:
        self._store: dict[str, tuple[float, Any]] = {}

    async def get(self, key: str) -> Any | None:
        entry = self._store.get(key)
        if entry is None:
            return None

        expires_at, value = entry
        if expires_at < time.time():
            self._store.pop(key, None)
            return None
        return value

    async def set(self, key: str, value: Any, ttl: int = 3600) -> None:
        self._store[key] = (time.time() + ttl, value)

    def clear(self) -> None:
        self._store.clear()


cache_manager = CacheManager()
