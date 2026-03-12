import asyncio
import websockets
import json
from websockets.exceptions import ConnectionClosed
from websockets import ClientConnection
from config import FURHAT_WS
from http_ollama import ollama_http

async def connect_to_server():
    async with websockets.connect(FURHAT_WS) as websocket:
        try:
            await furhat_startup(websockets)

            while True:
                data = await websocket.recv()
                data = json.loads(data)
                print("Init Data", data)

                if data["type"] == "response.attend.status":
                    if data["current"] != "nobody":
                        await websocket.send(json.dumps({
                            "type": "request.listen.start",
                            "partial": False,
                            "concat": True,
                            "stop_no_speech": True,
                            "stop_robot_start": True,
                            "stop_user_end": True,
                            "resume_robot_end": True
                        }))

                        while True:
                            data = await websocket.recv()
                            data = json.loads(data)
                            print("Second Data", data)

                            if data:
                                if data["type"] == "response.hear.end":
                                    response = await ollama_http(data["text"])

                                    await websocket.send(json.dumps({
                                        "type": "request.speak.text",
                                        "text": str(response)
                                    }))
                                
                                if data["type"] == "response.listen.end":
                                    if data["cause"] == "silence_timeout":
                                        break
        except ConnectionClosed:
            print("Server close")

async def furhat_startup(websocket: ClientConnection):
    # initiate language config
    await websocket.send(json.dumps({
        "type": "request.listen.config",
        "languages": [
            "en-US"
        ]
    }))
    
    # initiate furhat attention
    await websocket.send(json.dumps({"type": "request.attend.user"}))

    # make furhat speak at startup
    await websocket.send(json.dumps({
        "type": "request.speak.text",
        "text": "Huarghh Good Morning. Starting Up!"
    }))

if __name__ == "__main__":
    asyncio.run(connect_to_server())