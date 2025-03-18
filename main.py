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
from app.api import FootballAPI
from app.database_manager.database import Database
from app.cli_interface.cli import CLI
from app.web_interface.web import run_server

def update_data(use_test_data=False):
    """Fetch latest data from API (of test_data.json) and save to DB"""
    api = FootballAPI(use_test_data=use_test_data)
    db = Database(use_test_data=use_test_data)
    
    print("Fetching latest football match data...")
    try:
        matches = api.get_yesterdays_matches()
        db.save_matches(matches)
        print(f"Saved {len(matches)} match records.")
    except Exception as e:
        print(f"Error updating data: {str(e)}")

def prompt_interface_choice():
    """Prompt the user to choose an interface and validate the input."""
    while True:
        print("\nPlease choose your preffered interface:")
        print("1. CLI")
        print("2. Web Interface")
        choice = input("Enter your choide (1 or 2): ").strip()
        if choice in ("1", "2"):
            return choice
        else:
            print("Invalid input. Please enter '1' for CLI or '2' for Web Interface.\n")

def main():
    parser = argparse.ArgumentParser(description="goAI Talk")
    parser.add_argument("--update", action="store_true", help="Update match data")
    parser.add_argument("--test", action="store_true", help="TEST MODE: Use test data from test_data.json")
    args = parser.parse_args()

    db = Database(use_test_data=args.test)
    matches = db.get_yesterdays_matches_from_db()
    if not matches or args.update:
        update_data(use_test_data=args.test)

    choice = prompt_interface_choice()
    if choice == "2":
        print("Starting web server. Access at http://localhost:8000")
        run_server()
    else:
        cli = CLI()
        cli.run()

if __name__ == "__main__":
    main()
