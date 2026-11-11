"""FastAPI dependencies."""
from __future__ import annotations

from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)

security = HTTPBearer(auto_error=False)


async def get_api_key(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(security)],
) -> str:
    """Validate API key from Authorization header.

    For MVP, we accept any key if DEBUG is true, or require a specific key.
    """
    if settings.debug:
        return credentials.credentials if credentials else "dev-key"

    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API key",
        )

    # In production, validate against a real key store
    expected_key = settings.groq_api_key  # Simple fallback
    if credentials.credentials != expected_key:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API key",
        )

    return credentials.credentials


APIKey = Annotated[str, Depends(get_api_key)]