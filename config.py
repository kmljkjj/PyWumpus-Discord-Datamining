import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
PREFIX = "!"
OWNER_ID = int(os.getenv("OWNER_ID", "0"))

# Canaux de notifications
BUILD_CHANNEL = int(os.getenv("BUILD_CHANNEL", "0"))
EXP_CHANNEL = int(os.getenv("EXP_CHANNEL", "0"))
