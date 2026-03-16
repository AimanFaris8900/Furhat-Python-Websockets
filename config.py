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

#==== FURHAT CONFIG SETUP ======

LANGUAGE = "en-US"

#==== OLLAMA HTTP =======

OLLAMA_URL = os.getenv("OLLAMA_URL")
OLLAMA_LOCAL = os.getenv("OLLAMA_LOCAL")

#==== OLLAMA SETUP ====

MODEL = os.getenv("MODEL")