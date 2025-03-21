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
from typing import List, Dict, Any
from app.api import FootballAPI
from app.database_manager.database import Database
from app.cli_interface.cli import CLI
from app.web_interface.web import run_server
from config import settings

def update_data(use_test_data: bool = False) -> None:
    """Fetch latest data from API (of test_data.json) and save to DB

    Args:
         use_test_data (bool): Whether to usetest data instead of live API. Defaults to False.
    """
    api: FootballAPI = FootballAPI(settings, use_test_data=use_test_data)
    db: Database = Database(settings, use_test_data=use_test_data)
    
    print("Fetching latest football match data...")
    try:
        matches: List[dict[str, Any]] = api.get_yesterdays_matches()
        db.save_matches(matches)
        print(f"Saved {len(matches)} match records.")
    except Exception as e:
        print(f"Error updating data: {str(e)}")

def prompt_interface_choice() -> str:
    """Prompt the user to choose an interface and validate the input.

    Return:
        str: The user's chosen interface option ("1" or "2")
    """
    while True:
        print("\nPlease choose your prefered interface:")
        print("1. CLI")
        print("2. Web Interface")
        choice: str = input("Enter your choice (1 or 2): ").strip()
        if choice in ("1", "2"):
            return choice
        else:
            print("Invalid input. Please enter '1' for CLI or '2' for Web Interface.\n")

def main() -> None:
    parser: argparse.ArgumentParser = argparse.ArgumentParser(description="""goAI Talk - Football Match Results Q&A Bot that provides information 
                                     about yesterday's football matches through either a CLI or web interface. 
                                     \nUse --update to fetch the latest match data 
                                     or --test to run in test mode with sample data.
                                     """)
    parser.add_argument("--update", action="store_true", help="Update match data")
    parser.add_argument("--test", action="store_true", help="Test mode: Uses test data from tests/test_data.json")
    args: argparse.Namespace = parser.parse_args()

    db: Database = Database(settings)
    matches: List[Dict[str, Any]] = db.retrieve_yesterdays_matches_from_db()
    if not matches or args.update:
        update_data(use_test_data=args.test)

    choice: str = prompt_interface_choice()
    if choice == "2":
        print("Starting web server. Access at http://localhost:8000")
        run_server()
    else:
        cli = CLI(settings)
        cli.run()

if __name__ == "__main__":
    main()
