"""Development environment configuration."""

import os
from dotenv import load_dotenv

load_dotenv()

CONFIG = {
    "DEBUG": True,
    "LOG_LEVEL": "DEBUG",
    "API_TIMEOUT": 30,
    "CACHE_EXPIRY": 3600,
    "DATABASE": {
        "path": "database/football_matches.db"
    },
    "API_KEYS": {
        "FOOTBALL_API": os.getenv("FOOTBALL_API_KEY"),
        "OPENAI_API": os.getenv("OPENAI_API_KEY")
    }
}
