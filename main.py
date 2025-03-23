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

goAI Talk - Football Match Results Q&A Bot
File: main.py
Author: Hosu Kim
Created: 2025-03-15 20:17:52 UTC

Description:
    This module provides the FootballAPI class to interact with the football data API,
    fetching matches, goals, and related information.
'''
import argparse
from typing import List
from rich.console import Console
from app.api import FootballAPI
from app.database_manager.database import Database
from app.cli_interface.cli import CLI
from app.web_interface.web import run_server
from app.domain.domain import Match
from app.llm import QnAEngine
from config import settings
# Used for logging setup
import logging
from app.logging_config import setup_logging

def update_data(use_test_data: bool = False) -> None:
    """Fetch latest data from API (of test_data.json) and save to DB

    Args:
         use_test_data (bool): Whether to use test data instead of live API. Defaults to False.
    """
    api: FootballAPI = FootballAPI(settings, use_test_data=use_test_data)
    db: Database = Database(settings, use_test_data=use_test_data)
    
    logging.info("Fetching latest football match data...")
    try:
        matches: List[Match] = api.get_yesterdays_matches()
        db.save_matches(matches)
        logging.info(f"Saved {len(matches)} match records.")
    except Exception as e:
        logging.error(f"Error updating data: {str(e)}", exc_info=True)

def prompt_interface_choice() -> str:
    """Prompt the user to choose an interface and validate the input.

    Return:
        str: The user's chsen interface option ("1" for CLI or "2" for Web)
    """
    while True:
        logging.debug("Prompting user for interface choice")
        print("\nPlease choose your prefered interface:")
        print("1. CLI")
        print("2. Web Interface")
        choice: str = input("Enter your choice (1 or 2): ").strip()
        if choice in ("1", "2"):
            return choice
        else:
            logging.warning(f"Invalid interface choice: {choice}")
            print("Invalid input. Please enter '1' for CLI or '2' for Web Interface.\n")

def main() -> None:
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="""goAI Talk - Football Match Results Q&A Bot that provides information 
                       about yesterday's football matches through either a CLI or web interface.\n
                       Use --update to fetch the latest match data or --test to run in test mode with sample data."""
    )
    parser.add_argument("--update", action="store_true", help="Update match data")
    parser.add_argument("--test", action="store_true", help="Test mode: Uses test data from tests/test_data.json")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    parser.add_argument("--log-console", action="store_true", help="Show logs in console")
    args: argparse.Namespace = parser.parse_args()

    # Setup logging configuration
    setup_logging(debug_mode=args.debug, console_logs=args.log_console)

    logging.info("Starting goAI Talk application")
    logging.info(f"Command line arguments: update={args.update}, test={args.test}, debug={args.debug}")

    db: Database = Database(settings)
    matches: List[Match] = db.retrieve_yesterdays_matches_from_db()
    if not matches or args.update:
        logging.info("No matches found or update requested, fetching fresh data")
        update_data(use_test_data=args.test)

    choice: str = prompt_interface_choice()
    if choice == "2":
        logging.info("Starting web server. Access at http://localhost:8000")
        run_server()
    else:
        logging.info("Starting CLI interface")
        console: Console = Console()
        qna_engine: QnAEngine = QnAEngine(settings, db)
        cli: CLI = CLI(console, db, qna_engine)
        cli.run()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        # Setup basic logging in case the regular setup failed
        logging.basicConfig(level=logging.ERROR)
        logging.error("Unhandled exception in main", exc_info=True)
        print(f"An unexpected error occurred: {str(e)}")