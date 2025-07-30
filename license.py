import os
from dotenv import load_dotenv

def check_license():
    load_dotenv()
    token = os.getenv("BOT_TOKEN")
    channel = os.getenv("CHANNEL_ID")
    return token and channel
