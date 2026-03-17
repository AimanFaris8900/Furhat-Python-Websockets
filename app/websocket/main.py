import asyncio
import websockets
import json
import random
from websockets.exceptions import ConnectionClosed
from websockets import ClientConnection
from config import FURHAT_WS, LANGUAGE
from app.ollama.ollama_client import ollama_prompt

user_stat = {
    "stat" : "0"
}

# FUNC: Connect with Furhat through websocket
async def connect_to_server():
    async with websockets.connect(FURHAT_WS) as websocket:
        try:
            await furhat_startup(websocket)
            await furhat_speak(websocket, "How can I help you today?")

            while True:
                data = await websocket.recv()
                data = json.loads(data)
                print("Init Data", data)

                # update user presence
                update_stat(data)
                    
                if user_stat["stat"] != "nobody":
                    
                    await furhat_start_listen(websocket)
                    print("FURHAT START LISTEN")

                    while True:
                        if user_stat["stat"] != "nobody":
                            data = await websocket.recv()
                            data = json.loads(data)
                            print("Second Data", data)

                            # update user presence
                            update_stat(data)
                            print("USER STAT UPDATED 2nd: ", data)

                            if data:
                                if data["type"] == "response.hear.end":
                                    #response = await ollama_http(data["text"])
                                    response = await ollama_prompt(data["text"])

                                    await furhat_speak(websocket, str(response))
                                
                                if data["type"] == "response.listen.end":
                                    if data["cause"] == "silence_timeout":
                                        await furhat_start_listen(websocket)
                                        await furhat_speak(websocket, "You seems shy huh?")
                        else:
                            await furhat_stop_listen(websocket)
                            break

        except ConnectionClosed:
            print("Server close")

# FUNC: Furhat at startup
async def furhat_startup(websocket: ClientConnection):
    # initiate language config
    await websocket.send(json.dumps({
        "type": "request.listen.config",
        "languages": [
            LANGUAGE
        ]
    }))

    # make furhat speak at startup
    text = "Huarghh. Good Morning. Starting Up!"
    await furhat_speak(websocket, text)

    # initiate furhat attention
    await websocket.send(json.dumps({"type": "request.attend.user"}))

# FUNC: Furhat speak handler function
async def furhat_speak(websocket: ClientConnection, text: str):
    await websocket.send(json.dumps({
        "type": "request.speak.text",
        "text": text
    }))

async def furhat_start_listen(websocket: ClientConnection):
    await websocket.send(json.dumps({
        "type": "request.listen.start",
        "partial": False,
        "concat": True,
        "stop_no_speech": True,
        "stop_robot_start": True,
        "stop_user_end": True,
        "resume_robot_end": True
    }))

async def furhat_stop_listen(websocket: ClientConnection):
    await websocket.send(json.dumps({
        "type": "request.listen.stop"
    }))

def update_stat(data: dict):
    if data["type"] == "response.attend.status":
        user_stat.update({"stat" : data["current"]})

if __name__ == "__main__":
    asyncio.run(connect_to_server())
