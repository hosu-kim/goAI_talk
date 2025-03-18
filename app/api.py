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

goAI_talk - Yesterday's Football Match Results Q&A Bot
File: app/api.py
Author: Hosu Kim
Created: 2025-03-14 11:11:38 UTC

Description:
    This module provides the FootballAPI class to interact with the football data API,
    fetching matches, goals, and related information.
'''

import json
import config
import requests
from datetime import datetime, timedelta

class FootballAPI:
    """A client for interacting with the football data API.
    
    This class provides methods to fetch and process football match data
    from an external API service.

    Attributes:
        use_test_data (bool): Flag indicating wether to use test data instead of live API.
        base_url (str): Base URL for the football data API.
        api_key (str): Authentication key for the football data API.
        headers (dict): HTTP headers used for API requests.
    """
    def __init__(self, use_test_data=False):
        """Initialize the FootballAPI client.

        Args:
            use_test_data (bool, optional): If True, use local test data instead of making API calls.
            Defaults to False.
        """
        self.use_test_data = use_test_data
        self.base_url = config.API_FOOTBALL_URL
        self.api_key = config.API_FOOTBALL_KEY
        self.headers =  {
            "x-apisports-key": self.api_key
        }

    def get_yesterdays_matches(self):
        if self.use_test_data:
            return self._load_test_data()
        
        yesterday = (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d")
        endpoint = f"{self.base_url}/fixtures"
        params = {
            "date": yesterday,
            "status": "FT-AET-PEN"
        }
        
        print(f"\nFetching matches for {yesterday}...")
        
        try:
            response = requests.get(
                endpoint,
                headers=self.headers,
                params=params
            )
            print(f"API Response Status: {response.status_code}")
            
            if response.status_code != 200:
                print(f"API Error: {response.text}")
                return []
                
            data = response.json()
            if 'response' not in data:
                print("Unexpected API response format")
                print(f"Response: {data}")
                return []
                
            matches = self._process_match_data(data['response'])
            print(f"Retrieved {len(matches)} matches")
            
            return matches
            
        except Exception as e:
            print(f"API request failed: {str(e)}")
            return []

    """=========================== TEST DATA LOAD ==========================="""
    def _load_test_data(self):
        """Loads match data from a local test file for development purposes.
        
        Returns:
            list: A list of dictionaries containing processed match data.

        Raises:
            FileNotFoundError: If the test_data.json file doesn't exist.
            json.JSONDecodeError: if the file contains ivalid JSON.
        """
        with open('tests/test_data.json', 'r') as file:
            test_data = json.load(file)
        return self._process_match_data(test_data['response'])

    def _process_match_data(self, data):
        """Transforms raw API match data into a structured format.
        
        Args:
            data (list): A list of dictionaries containing raw match data from the API.

        Returns:
            list: A list of dictionaries with processed match information including
                  team details, scores, and goal information when available.
        """
        processed_data = []
        for match in data:
            processed_match = {
                "match_id": match['fixture']['id'],
                "date": match['fixture']['date'],
                "league": match['league']['name'],
                "country": match['league']['country'],
                "home_team": match['teams']['home']['name'],
                "away_team": match['teams']['away']['name'],
                "home_score": match['goals']['home'],
                "away_score": match['goals']['away'],
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
