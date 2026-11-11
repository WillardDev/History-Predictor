"""Debug test for Groq JSON mode return type."""
import asyncio
import json
import os
from groq import AsyncGroq

async def test_json_mode():
    client = AsyncGroq(api_key=os.environ["GROQ_API_KEY"])
    response = await client.chat.completions.create(
        model="qwen/qwen3.8-27b",
        messages=[
            {"role": "system", "content": "Return valid JSON only."},
            {"role": "user", "content": 'Return: {"name": "test", "value": 42}'}
        ],
        temperature=0.7,
        max_tokens=100,
        response_format={"type": "json_object"},
    )
    content = response.choices[0].message.content
    print(f"Type: {type(content)}")
    print(f"Value: {content}")
    if isinstance(content, str):
        parsed = json.loads(content)
        print(f"Parsed: {parsed}")
    else:
        print(f"Already dict: {content}")

asyncio.run(test_json_mode())
