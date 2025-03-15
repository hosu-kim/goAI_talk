#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
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

goAI_talk - Football Match Results Q&A Bot
File: utils/config.py
Author: hosu-kim
Created: 2025-03-14 11:05:33 UTC

Description:
    This module provides configuration functionality for the application.
    It handles loading environment variables, setting up loggers, and configuration files.
"""
import os
import logging
from dotenv import load_dotenv
import json
from typing import Dict, Any

# Try to import LOG_LEVELS from constants, but provide fallback if not available
try:
    from utils.constants import LOG_LEVELS
except ImportError:
    # Fallback logging levels if import fails
    LOG_LEVELS = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL
    }

def load_config() -> Dict[str, Any]:
    """Load and validate configuration settings."""
    load_dotenv()
    
    config = {
        # API keys
        "football_api_key": os.getenv("FOOTBALL_API_KEY"),
        "openai_api_key": os.getenv("OPENAI_API_KEY"),
        
        # Application settings
        "debug": os.getenv("DEBUG", "False").lower() == "true",
        "log_level": os.getenv("LOG_LEVEL", "INFO").upper(),
        "user_timezone": os.getenv("USER_TIMEZONE", "UTC"),
        "max_matches": int(os.getenv("MAX_MATCHES", "30")),
        "openai_model": os.getenv("OPENAI_MODEL", "gpt-3.5-turbo"),
        
        # Database settings
        "db_dir": os.getenv("DB_DIR", "database"),
        "db_name": os.getenv("DB_NAME", "football_matches.db"),
        
        # Logging settings
        "log_dir": os.getenv("LOG_DIR", "logs"),
    }
    
    # Complete DB path
    config["db_path"] = os.path.join(config["db_dir"], config["db_name"])
    
    # Set log level
    config["log_level_enum"] = LOG_LEVELS.get(config["log_level"], logging.INFO)
    
    required_keys = ["football_api_key", "openai_api_key"]
    missing_keys = [key for key in required_keys if not config.get(key)]
    if missing_keys:
        raise ValueError(f"Missing required configuration keys: {', '.join(missing_keys)}")
        
    # Validate values
    if config["max_matches"] < 1:
        raise ValueError("max_matches must be greater than 0")
        
    return config

def setup_logger(name, log_file=None):
    """Unified logger setup function that uses a single log directory.
    
    Args:
        name: The name of the logger
        log_file: Optional specific log filename, defaults to name.log
        
    Returns:
        A configured logger instance
    """
    config = load_config()
    log_dir = config["log_dir"]
    
    # Ensure log directory exists
    os.makedirs(log_dir, exist_ok=True)
    
    # Set default log file name if not provided
    if not log_file:
        log_file = f"{name}.log"
    
    log_path = os.path.join(log_dir, log_file)
    
    logger = logging.getLogger(name)
    logger.setLevel(config["log_level_enum"])
    
    # Add handlers only if they don't exist
    if not logger.handlers:
        # File handler
        file_handler = logging.FileHandler(log_path)
        file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
        
        # Add console handler only in debug mode
        if config["debug"]:
            console_handler = logging.StreamHandler()
            console_formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
            console_handler.setFormatter(console_formatter)
            logger.addHandler(console_handler)
    
    return logger

def load_additional_config(config_path="config.json"):
    """Load additional configuration from JSON file"""
    default_config = {
        "version": "1.0.0",
        "language": "en",
        "default_timezone": "UTC",
        "max_cache_age_hours": 12,
        "preferred_leagues": [
            "Premier League",
            "La Liga",
            "Serie A",
            "Bundesliga",
            "Ligue 1"
        ],
        "max_results": 10,
        "api_settings": {
            "openai": {
                "temperature": 0.3,
                "max_tokens": 800
            }
        }
    }
    
    try:
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as config_file:
                user_config = json.load(config_file)
                merged_config = {**default_config, **user_config}
                
                if "api_settings" in user_config:
                    merged_config["api_settings"] = {
                        **default_config.get("api_settings", {}),
                        **user_config["api_settings"]
                    }
                
                return merged_config
        else:
            logging.warning(f"Configuration file {config_path} not found. Using default configuration.")
            return default_config
    except Exception as e:
        logging.error(f"Error loading configuration: {str(e)}")
        return default_config