import asyncio
from ollama import AsyncClient
from config import OLLAMA_LOCAL, MODEL

messages = []

async def ollama_init(ollama_client: AsyncClient):
    client = ollama_client(host=OLLAMA_LOCAL)
    return client

async def ollama_prompt(prompt: str):
    print(OLLAMA_LOCAL)
    client = AsyncClient(host=OLLAMA_LOCAL)

    messages.append({
        'role': 'user', 'content': prompt
    })

    response = await client.chat(model=MODEL, messages=messages)

    answer = response.message.content

    messages.append(
        {'role': 'assistant', 'content': answer}
    )

    return answer


if __name__ == "__main__":
    asyncio.run(ollama_prompt(prompt="Hello"))