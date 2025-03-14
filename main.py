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
from api.football_api import FootballAPI
from database.database_manager import DBManager
from llm.qna_engine import QnAEngine
from interface.cli import FootballQnACLI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup application logger
logger = setup_logger("main")

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
        args = parser.parse_args()

        # Load additional configurations
        additional_config = load_additional_config(args.config)
        logger.info(f"Loaded additional configurations from {args.config}")
        
        # Display startup information
        print(f"\n{'-'*60}")
        print(f"Football Match Results Q&A Bot - v{additional_config.get('version', '1.0.0')}")
        print(f"Started at: {get_current_time()}")
        print(f"Mode: {'Web' if args.web else 'CLI'}")
        print(f"{'-'*60}\n")
        
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
            cli = FootballQnACLI(football_api, data_manager, qna_engine, user_location=user_location)
            cli.start()
        
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
