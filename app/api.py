"""Interperter and Encoding setup"""
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
File: app/api.py
Author: Hosu Kim
Created: 2025-03-14 11:11:38 UTC

Description:
    This module provides the FootballAPI class to interact with the football data API,
    fetching matches, goals, and related information.
'''
import json # Used to import test_data for testing.
import os # Used to interact with the OS.
from dotenv import load_dotenv # Used to import API base URL and keys from .env
import requests # Used to send HTTP requests and handle responses.
from datetime import datetime, timedelta # Used for calcuating time differences.

load_dotenv()

BASE_URL = os.getenv('FOOTBALL_BASE_URL')
API_FOOTBALL_KEY = os.getenv('FOOTBALL_API_KEY')

class FootballAPI:
    """A client for interacting with the football data API.
    
    This class provides methods to fetch and process football match data
    from an external API service.
    """
    def __init__(self):
        self.base_url = BASE_URL
        self.api_key = API_FOOTBALL_KEY
        self.headers =  {
            "x-apisports-key": self.api_key
        }
    '''=========================== API CALL METHOD ==========================='''
    def get_yesterdays_matches(self):
        """Fetches yesterday's match results from the API.
        
        Returns:
            A list of dictionaries containing processed match data.

        Raises:
            Exception: If the API request fails.
        """
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        endpoint = f"{self.base_url}/fixtures"
        params = {"date": yesterday}

        response = requests.get(endpoint, headers=self.headers, params=params)
        
        if response.status_code == 200: # HTTP call success
            return self._process_match_data(response.json()['response'])
        else:
            raise Exception(f"API request failed: {response.status_code}")
    

    """=========================== TEST DATA LOAD ==========================="""
    def _load_test_data(self):
        """Loads match data from a local test file for development purposes.
        
        Returns:
            A list of dictionaries containing processed match data.
        """
        with open('test_data.json', 'r') as file:
            test_data = json.load(file)
        return self._process_match_data(test_data['response'])

    def _process_match_data(self, data):
        """Transforms raw API match data into a structured format.
        
        Args:
            data: A list of dictionaries containing raw match data.

        Returns:
            A list of dictionaries with processed match information including
            team details, scores, and goal information when available.
        """
        processed_data = []
        for match in data:
            processed_match = {
                "match_id": match['fixture']['id'],
                "date": match['fixture'],
                "league": match['league']['name'],
                "home_team": match['teams']['home']['name'],
                "away_team": match['teams']['away']['name'],
                "home_team_score": match['goals']['home'],
                "away_team_score": match['goals']['away'],
                "status": match['fixture']['status']['short']
            }

            # Add goal information
            if 'events' in match and match['events']:
                goals = []
                for event in match['events']:
                    if event['type'] == 'Goal':
                        goals.append({
                            "team": event['team']['name'],
                            "player": event['player']['name'],
                            "minute": event['time']['elapsed']
                        })
                processed_match['goals'] = goals

            processed_data.append(processed_match)
        return processed_data
