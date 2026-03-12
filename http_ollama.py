import httpx
import asyncio
from config import OLLAMA_URL, MODEL

async def ollama_http(prompt: str):
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    }

    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(OLLAMA_URL, json=payload)
        data = response.json()

        return data["response"]
        #print(data["response"])

if __name__ == "__main__":
    asyncio.run(ollama_http("HELLO"))
