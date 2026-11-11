"""Quick test to list available Groq models."""
import asyncio
import os
from groq import AsyncGroq

async def list_models():
    client = AsyncGroq(api_key=os.environ["GROQ_API_KEY"])
    try:
        models = await client.models.list()
        print("Available models:")
        for m in models.data:
            print(f"  - {m.id}")
    except Exception as e:
        print(f"Error: {e}")

asyncio.run(list_models())
