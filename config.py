import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# API-Football url
API_FOOTBALL_URL = "https://v3.football.api-sports.io"

# API keys
API_FOOTBALL_KEY = os.getenv("API_FOOTBALL_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Database settings
DB_PATH = os.getenv("DB_PATH", "football_data.db")

# Applicatin constants
MATCH_LIMIT = 300

MAX_CONVERSATION_HISTORY = 5