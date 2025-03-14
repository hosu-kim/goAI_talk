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

def load_config():
	"""Load environment variables and configuration settings."""
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
	}
	
	# Complete DB path
	config["db_path"] = os.path.join(config["db_dir"], config["db_name"])
	
	# Set log level
	log_levels = {
		"DEBUG": logging.DEBUG,
		"INFO": logging.INFO,
		"WARNING": logging.WARNING,
		"ERROR": logging.ERROR,
		"CRITICAL": logging.CRITICAL
	}
	config["log_level_enum"] = log_levels.get(config["log_level"], logging.INFO)
	
	return config

def load_additional_config(json_path):
	"""Load additional configuration from a JSON file."""
	if os.path.exists(json_path):
		with open(json_path, 'r') as f:
			return json.load(f)
	return {}

def setup_logger(name, log_dir="logs"):
	"""Unified logger setup function."""
	config = load_config()
	
	os.makedirs(log_dir, exist_ok=True)
	log_file = os.path.join(log_dir, f"{name}.log")
	
	logger = logging.getLogger(name)
	logger.setLevel(config["log_level_enum"])
	
	# Add handlers only if they don't exist
	if not logger.handlers:
		# File handler
		file_handler = logging.FileHandler(log_file)
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