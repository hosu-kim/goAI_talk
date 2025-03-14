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
File: main.py
Author: hosu-kim
Created: 2025-03-14 09:38:22 UTC

Description:
    This is the main entry point for the goAI_talk application.
    The application provides a Q&A interface for football match results
    with support for both CLI and web interfaces.
"""

import argparse
import os
import sys
import traceback
import time
from datetime import datetime, timedelta, timezone
import json
from colorama import Fore, Style, init

from api.football_api import FootballAPI
from database.database_manager import DBManager
from llm.qna_engine import QnAEngine
from interface.cli import FootballQnACLI
from dotenv import load_dotenv
from utils.config import setup_logger, load_additional_config
from utils.data_utils import get_current_time
from utils.data_fetcher import fetch_matches
from football_api import fetch_matches_for_date
from chat_engine import process_question

# Initialize colorama
init()

# Load environment variables
load_dotenv()

# Setup application logger
logger = setup_logger("main")

# Constants
DEFAULT_DAYS = 7  # Default number of days to fetch
DATA_DIR = "data"
CACHE_FILE = os.path.join(DATA_DIR, "match_cache.json")

def check_api_keys():
    """Check if necessary API keys are present."""
    football_api_key = os.getenv("FOOTBALL_API_KEY")
    openai_api_key = os.getenv("OPENAI_API_KEY")
    
    missing_keys = []
    if not football_api_key:
        missing_keys.append("FOOTBALL_API_KEY")
    if not openai_api_key:
        missing_keys.append("OPENAI_API_KEY")
        
    if missing_keys:
        print(f"ERROR: Missing required API key(s): {', '.join(missing_keys)}")
        print("Please add them to your .env file and try again.")
        return False
        
    return True

def handle_user_input(user_input, matches_data):
    if user_input.lower().startswith('date '):
        try:
            new_date = user_input.split(' ')[1]
            datetime.strptime(new_date, '%Y-%m-%d')  # Validate date format
            return fetch_matches(new_date)
        except (IndexError, ValueError):
            print("Invalid date format. Please use YYYY-MM-DD")
            return matches_data
    # ...existing code...

def ensure_data_dir():
    """Ensure the data directory exists"""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

def load_cached_data():
    """Load cached match data if available"""
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, 'r') as f:
                cache_data = json.load(f)
                last_updated = cache_data.get('last_updated')
                matches = cache_data.get('matches', [])
                
                # Convert last_updated to datetime
                if last_updated:
                    last_updated = datetime.fromisoformat(last_updated)
                    
                return matches, last_updated
        except Exception as e:
            print(f"Error loading cache: {e}")
    
    return [], None

def save_cache(matches):
    """Save matches data to cache file"""
    ensure_data_dir()
    cache_data = {
        'last_updated': datetime.utcnow().isoformat(),
        'matches': matches
    }
    
    with open(CACHE_FILE, 'w') as f:
        json.dump(cache_data, f)

def fetch_recent_matches(days=DEFAULT_DAYS, force=False):
    """Fetch matches for the last N days"""
    matches, last_updated = load_cached_data()
    
    # Check if cache is recent (less than 6 hours old) and not forcing refresh
    cache_valid = (last_updated and 
                  (datetime.utcnow() - last_updated).total_seconds() < 21600 and 
                  not force)
    
    if matches and cache_valid:
        print(f"Using cached match data (last updated: {last_updated.strftime('%Y-%m-%d %H:%M:%S')} UTC)")
        return matches
    
    # Fetch fresh data
    all_matches = []
    today = datetime.utcnow().date()
    
    print(f"Fetching match data for the last {days} days...")
    
    for i in range(days):
        target_date = today - timedelta(days=i)
        date_str = target_date.strftime("%Y-%m-%d")
        
        print(f"Fetching matches for date: {date_str}")
        day_matches = fetch_matches_for_date(date_str)
        
        if day_matches:
            all_matches.extend(day_matches)
        
        # Respect API rate limits
        if i < days - 1:
            time.sleep(1)
    
    # Save to cache
    if all_matches:
        save_cache(all_matches)
    
    return all_matches

def display_banner():
    print("╭────────────────────────────────────────────────╮")
    print("│ Football Matches Q&A Bot                       │")
    print("│ Ask me anything about recent football matches! │")
    print("╰────────────────────────────────────────────────╯")
    print(f"Current Date and Time (UTC): {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}\n")
    print("type 'help' for available commands or 'exit' to quit.\n")
    print(f"User Location: UTC")

def cli_interface(matches):
    """Command line interface for the chat bot"""
    display_banner()
    
    while True:
        try:
            user_input = input("\nAsk me about football matches: ")
            
            if not user_input.strip():
                continue
                
            if user_input.lower() == 'exit':
                print("Goodbye!")
                break
                
            if user_input.lower() == 'help':
                print("\nCommands:")
                print("  help - Show this help message")
                print("  exit - Exit the program")
                print("  refresh - Refresh match data")
                print("\nExample questions:")
                print("  'Who won the Manchester United game yesterday?'")
                print("  'Show me all Premier League results from this week'")
                print("  'What was the score in the Barcelona match?'")
                continue
                
            if user_input.lower() == 'refresh':
                print("Refreshing match data...")
                matches = fetch_recent_matches(force=True)
                print(f"Successfully refreshed data. {len(matches)} matches available.")
                continue
            
            print("Thinking...")
            if not matches:
                print("No match data available. Fetching fresh data...")
                matches = fetch_recent_matches()
                if not matches:
                    print("Couldn't retrieve match data. Please check your internet connection and API access.")
                    continue
            
            answer = process_question(user_input, matches)
            print(f"\n{Fore.GREEN}{answer}{Style.RESET_ALL}")
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")

def main():
    """
    Main entry point for the goAI_talk application.

    This function parses command-line arguments, initializes the required
    components (FootballAPI, DBManager, QnAEngine), and starts the appropriate
    interface (CLI or web). If the fetch flag is provided, yesterday's match data
    is also fetched and saved to the database.

    Raises:
        Exception: Propagates any exceptions encountered during initialization or execution.
    """
    # Check if required API keys are available
    if not check_api_keys():
        return 1
        
    try:
        # Parse command line arguments
        parser = argparse.ArgumentParser(description="Football Match Results Q&A Bot")
        parser.add_argument("--fetch", action="store_true", help="Fetch yesterday's match data")
        parser.add_argument("--web", action="store_true", help="Run web interface instead of CLI")
        parser.add_argument("--port", type=int, default=8000, help="Port for web interface")
        parser.add_argument("--debug", action="store_true", help="Run in debug mode")
        parser.add_argument("--config", type=str, default="config.json", help="Path to config file")
        parser.add_argument("--days", type=int, default=DEFAULT_DAYS,
                          help=f"Number of days of match data to fetch (default: {DEFAULT_DAYS})")
        args = parser.parse_args()

        # Display startup information
        print(f"\n{'-'*60}")
        print(f"Football Match Results Q&A Bot - v1.0.0")
        print(f"Started at: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Mode: {'Web' if args.web else 'CLI'}")
        print(f"{'-'*60}\n")
        
        if args.fetch:
            print("Fetching fresh match data...")
            matches = fetch_recent_matches(days=args.days, force=True) 
        else:
            matches = fetch_recent_matches(days=args.days)

        print(f"Successfully fetched {len(matches)} matches.")
        print("Starting CLI interface...")
        
        cli_interface(matches)

        # The rest of the function is preserved for future implementation
        try:
            # Load additional configurations
            additional_config = load_additional_config(args.config)
            logger.info(f"Loaded additional configurations from {args.config}")
            
            # Initialize components
            football_api = FootballAPI()
            data_manager = DBManager()
            qna_engine = QnAEngine()
            
            # Apply additional configurations if needed
            if 'api_settings' in additional_config:
                if 'openai' in additional_config['api_settings']:
                    openai_settings = additional_config['api_settings']['openai']
                    if 'temperature' in openai_settings:
                        qna_engine.temperature = openai_settings['temperature']
                    if 'max_tokens' in openai_settings:
                        qna_engine.max_tokens = openai_settings['max_tokens']

            # Check if fetch flag is set
            if args.fetch:
                print("Fetching yesterday's match data...")
                try:
                    matches = football_api.fetch_yesterday_matches(data_manager)
                    print(f"Successfully fetched {len(matches)} matches.")
                except Exception as e:
                    logger.error(f"Error fetching match data: {str(e)}")
                    print(f"Error fetching match data: {str(e)}")

            # Determine which interface to run
            if args.web:
                # Import web interface module only when needed
                from interface.web import run_web_app
                print("Starting web interface...")
                try:
                    run_web_app(data_manager, qna_engine, port=args.port, debug=args.debug)
                except Exception as e:
                    logger.error(f"Error running web interface: {str(e)}")
                    print(f"Error running web interface: {str(e)}")
                    return 1
            else:
                # Start CLI interface
                print("Starting CLI interface...")
                user_location = additional_config.get('default_timezone', 'UTC')
                cli = FootballQnACLI(football_api, data_manager, qna_engine, 
                                   user_location=user_location,
                                   use_test_data=args.debug)
                cli.start()
        except Exception as e:
            # If there's an error in the advanced setup, we can still fall back to the simple CLI
            print(f"Note: Advanced features unavailable - {str(e)}")
            pass
            
        return 0
    
    except KeyboardInterrupt:
        logger.info("Application terminated by user (Keyboard Interrupt)")
        print("\nApplication terminated by user.")
        return 0
    
    except Exception as e:
        logger.error(f"Unhandled exception: {str(e)}", exc_info=True)
        print(f"ERROR: An unexpected error occurred: {str(e)}")
        print("\nStack trace:")
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
