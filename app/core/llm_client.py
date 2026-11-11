"""Unified LLM client for Groq API."""
from __future__ import annotations

import json
import logging
from typing import Any, AsyncIterator

from groq import AsyncGroq
from groq import APIError as GroqAPIError

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class LLMClient:
    """Async client for Groq LLM API with structured output support."""

    def __init__(self) -> None:
        self.client = AsyncGroq(api_key=settings.groq_api_key)
        self.model = settings.groq_model
        self.temperature = settings.groq_temperature
        self.max_tokens = settings.groq_max_tokens

    async def generate(
        self,
        prompt: str,
        system_prompt: str | None = None,
        temperature: float | None = None,
        max_tokens: int | None = None,
        json_mode: bool = False,
    ) -> str:
        """Generate a text completion from the LLM.

        Args:
            prompt: The user prompt.
            system_prompt: Optional system prompt.
            temperature: Override temperature.
            max_tokens: Override max tokens.
            json_mode: If True, request JSON output format.

        Returns:
            The generated text.
        """
        messages: list[dict[str, str]] = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        kwargs: dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature if temperature is not None else self.temperature,
            "max_tokens": max_tokens if max_tokens is not None else self.max_tokens,
        }

        if json_mode:
            kwargs["response_format"] = {"type": "json_object"}

        try:
            response = await self.client.chat.completions.create(**kwargs)
            content = response.choices[0].message.content
            if content is None:
                raise ValueError("Empty response from LLM")
            return content.strip()
        except GroqAPIError as e:
            logger.error(f"Groq API error: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected LLM error: {e}")
            raise

    async def generate_json(
        self,
        prompt: str,
        system_prompt: str | None = None,
        schema: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Generate a JSON completion from the LLM.

        Args:
            prompt: The user prompt.
            system_prompt: Optional system prompt.
            schema: Optional JSON schema for validation.

        Returns:
            Parsed JSON response.
        """
        full_system = system_prompt or ""
        if schema:
            schema_str = json.dumps(schema, indent=2)
            full_system += f"\n\nYou MUST respond with valid JSON matching this schema:\n{schema_str}"

        content = await self.generate(
            prompt=prompt,
            system_prompt=full_system,
            json_mode=True,
        )

        try:
            return json.loads(content)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {e}\nContent: {content}")
            # Try to extract JSON from markdown code blocks
            if "```json" in content:
                json_str = content.split("```json")[1].split("```")[0]
                return json.loads(json_str)
            if "```" in content:
                json_str = content.split("```")[1]
                return json.loads(json_str)
            raise

    async def stream(
        self,
        prompt: str,
        system_prompt: str | None = None,
    ) -> AsyncIterator[str]:
        """Stream a text completion from the LLM.

        Args:
            prompt: The user prompt.
            system_prompt: Optional system prompt.

        Yields:
            Text chunks as they arrive.
        """
        messages: list[dict[str, str]] = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        try:
            stream = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                stream=True,
            )
            async for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        except GroqAPIError as e:
            logger.error(f"Groq streaming error: {e}")
            raise


# Singleton instance
llm_client = LLMClient()