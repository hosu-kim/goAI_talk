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
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Any
from config import Settings

class FootballAPI:
    """A client for interacting with the football data API.
    
    This class provides methods to fetch and process football match data
    from an external API service.

    Attributes:
        use_test_data (bool): Flag indicating wether to use test data instead of live API.
        base_url (str): Base URL for the football data API.
        api_key (str): Authentication key for the football data API.
        headers (Dict[str, str]): HTTP headers used for API requests.
    """
    use_test_data: bool
    config: Settings
    headers: Dict[str, str]

    def __init__(self, config: Settings, use_test_data: bool = False) -> None:
        """Initialize the FootballAPI client.

        Args:
            config (Settings): configuration settings object.
            use_test_data (bool, optional): If True, use local test data instead of making API calls.
            Defaults to False.
        """
        self.config = config
        self.use_test_data = use_test_data
        self.headers =  {
            "x-apisports-key": self.config.api_football_key.get_secret_value()
        }

    def get_yesterdays_matches(self) -> List[Dict[str, Any]]:
        """Retrieves football matches from yesterday.

        Fetches data either from the API or from test data based on configuration.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries containing match information.
        """
        if self.use_test_data:
            return self._load_test_data()

        yesterday: str = (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d")
        endpoint: str = f"{self.config.api_football_url}/fixtures"
        params: Dict[str, str] = {
            "date": yesterday,
            "status": "FT-AET-PEN"
        }

        print(f"\nFetching matches for {yesterday}...")

        try:
            response: requests.Response = requests.get(
                endpoint,
                headers=self.headers,
                params=params
            )
            print(f"API Response Status: {response.status_code}")

            if response.status_code != 200:
                print(f"API Error: {response.text}")
                return []

            data: Dict[str, Any] = response.json()
            if 'response' not in data:
                print("Unexpected API response format")
                print(f"Response: {data}")
                return []

            matches: List[Dict[str, Any]] = self._process_match_data(data['response'])
            print(f"Retrieved {len(matches)} matches")

            return matches

        except Exception as e:
            print(f"API request failed: {str(e)}")
            return []

    """=========================== TEST DATA LOAD ==========================="""
    def _load_test_data(self) -> List[Dict[str, Any]]:
        """Loads match data from a local test file for development purposes.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries containing processed match data.

        Raises:
            FileNotFoundError: If the test_data.json file doesn't exist.
            json.JSONDecodeError: if the file contains invalid JSON.
        """
        with open('tests/test_data.json', 'r') as file:
            test_data: Dict[str, Any] = json.load(file)
        return self._process_match_data(test_data['response'])

    def _process_match_data(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Transforms raw API match data into a structured format.

        Args:
            data (list[Dict[str, Any]]): A list of dictionaries containing raw match data from the API.

        Returns:
            list[Dict[str, Any]]: A list of dictionaries with processed match information including
                  team details, scores, and goal information when available.
        """
        processed_data: List[Dict[str, Any]] = []
        for match in data:
            processed_match: Dict[str, Any] = {
                "match_id": match['fixture']['id'],
                "date": match['fixture']['date'],
                "league": match['league']['name'],
                "country": match['league']['country'],
                "home_team": match['teams']['home']['name'],
                "away_team": match['teams']['away']['name'],
                "home_score": match['goals']['home'],
                "away_score": match['goals']['away']
            }

            # Add goal information if exists
            if 'events' in match and match['events']:
                goals: List[Dict[str, Any]] = []
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
