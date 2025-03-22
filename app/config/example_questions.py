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

goAI_talk - Football Match Results Q&A Bot
File: app/config/example_questions.py
Author: Hosu Kim
Created: 2025-03-22 10:13:59 UTC

Description:
    Defines example questions for web.py 
	to assist in football match result queries.
'''

EXAMPLE_QUESTIONS = {
    "Match Results": [
        "What were yesterday's match results?",
        "How many matches ended in a home win?",
        "Which teams kept a clean sheet yesterday?"
    ],
    "Score Details": [
        "Which match had the highest score?",
        "What was the halftime score in the CSA match?",
        "Were there any matches that went to extra time?"
    ],
    "League Information": [
        "Show me all CONCACAF Champions League matches",
        "What matches were played in the Copa Do Brasil?",
        "How many different leagues had matches yesterday?"
    ],
    "Venue & Location": [
        "Which matches were played in Brazil?",
        "What matches were played at Independence Park?",
        "Show me all match venues and their cities"
    ],
    "Team Performance": [
        "Did Inter Miami win their match?",
        "Which team scored the most goals in a single match?",
        "Show me all matches where the home team won"
    ]
}
