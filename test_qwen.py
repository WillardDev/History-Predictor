"""Quick test for qwen model JSON mode."""
import asyncio
import json
import os
from groq import AsyncGroq

async def test_qwen():
    client = AsyncGroq(api_key=os.environ["GROQ_API_KEY"])
    try:
        # Test basic completion
        response = await client.chat.completions.create(
            model="qwen/qwen3.8-27b",
            messages=[{"role": "user", "content": "Say hello in one sentence"}],
            temperature=0.7,
            max_tokens=100,
        )
        print(f"Basic: {response.choices[0].message.content}")
        
        # Test JSON mode
        try:
            response2 = await client.chat.completions.create(
                model="qwen/qwen3.8-27b",
                messages=[{"role": "user", "content": 'Return JSON: {"name": "test", "value": 42}'}],
                temperature=0.7,
                max_tokens=100,
                response_format={"type": "json_object"},
            )
            print(f"JSON mode: {response2.choices[0].message.content}")
        except Exception as e:
            print(f"JSON mode failed: {e}")
            
    except Exception as e:
        print(f"Error: {e}")

asyncio.run(test_qwen())
