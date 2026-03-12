from dotenv import load_dotenv
import os

load_dotenv()

#==== FURHAT HTTP ======

FURHAT_IP = os.getenv("FURHAT_IP")
FURHAT_LAN_IP = os.getenv("FURHAT_LAN_IP")

FURHAT_URL = os.getenv("FURHAT_URL")
FURHAT_LAN_URL = os.getenv("FURHAT_LAN_URL")

#==== FURHAT WEBSOCKET ======

FURHAT_WS = os.getenv("FURHAT_WS")

OLLAMA_URL = os.getenv("OLLAMA_URL")