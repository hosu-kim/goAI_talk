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

load_dotenv()

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
    parser = argparse.ArgumentParser(description="Football Match Results Q&A Bot")
    parser.add_argument("--fetch", action="store_true", help="Fetch yesterday's match data")
    parser.add_argument("--web", action="store_true", help="Run web interface instead of CLI")
    args = parser.parse_args()

    football_api = FootballAPI()
    data_manager = DBManager()
    qna_engine = QnAEngine()

    # Check if fetch flag is set
    if args.fetch:
        print("Fetching yesterday's match data...")
        football_api.fetch_yesterday_matches(data_manager)

    # Determine which interface to run
    if args.web:
        # Import web interface module only when needed
        from interface.web import run_web_app
        print("Starting web interface...")
        run_web_app(data_manager, qna_engine)
    else:
        # Start CLI interface
        print("Starting CLI interface...")
        cli = FootballQnACLI(football_api, data_manager, qna_engine)
        cli.start()

if __name__ == "__main__":
    main()
