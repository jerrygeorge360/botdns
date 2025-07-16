import os
from dotenv import load_dotenv

load_dotenv()

INSIGHT_API_BASE = os.getenv("INSIGHT_API_BASE", "http://localhost:5000")
