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
File: app.py
Author: hosu-kim
Created: 2025-03-14 09:45:30 UTC

Description:
    Main application entry point for goAI_talk.
    Handles user interface and coordinates between API and AI components.
"""

import logging
from datetime import datetime
from api import football_api

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Main application entry point"""
    logger.info("Starting goAI_talk application")
    
    # Example API call
    today = datetime.now().strftime("%Y-%m-%d")
    matches = football_api.get_matches(date_from=today, date_to=today)
    
    if "error" in matches:
        logger.error(f"Failed to fetch matches: {matches['error']}")
    else:
        logger.info(f"Successfully retrieved {len(matches.get('matches', []))} matches")
    
    # Application logic would continue here
    
if __name__ == "__main__":
    main()
