
#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
          ___
      .:::---:::.
    .'--:     :--'.                      ___     ____   ______        __ __  
   /.'   \   /   `.\      ____ _ ____   /   |   /  _/  /_  __/____ _ / // /__
  | /'._ /:::\ _.'\ |    / __ `// __ \ / /| |   / /     / /  / __ `// // //_/
  |/    |:::::|    \|   / /_/ // /_/ // ___ | _/ /     / /  / /_/ // // ,<   
  |:\ .''-:::-''. /:|   \__, / \____//_/  |_|/___/    /_/   \__,_//_//_/|_|  
   \:|    `|`    |:/   /____/                                                
    '.'._.:::._.'.'
      '-:::::::-'

goAI_talk - Yesterday's Football Match Results Q&A Bot
File: config.py
Author: Hosu Kim
Created: 2025-03-19 16:42:29 UTC

Description:
    Configuration settings for goAI_talk using Pydantic for type validation
    and environment variable management.
'''

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr

class Settings(BaseSettings):
    """Application configuration settings loaded from environment variables.

    Use Pydantic BaseSettings to load values from .env file and environment variables.
    Secret values are wrapped with SecretStr for better security handling.
    """
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)

    api_football_url: str = "https://v3.football.api-sports.io"
    api_football_key: SecretStr
    openai_api_key: SecretStr
    db_path: str = "app/database_manager/football_data.db"

    match_limit: int = 300 # Maximum number of matches to process at once
    max_conversation_history: int = 5 # Number of conversation turns to retain

settings = Settings()