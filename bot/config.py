# config.py
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TG_API_TOKEN")
INSIGHT_API_BASE = os.getenv("INSIGHT_API_BASE", "http://localhost:5000")
