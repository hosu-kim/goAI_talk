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
File: tests/test_api.py
Author: Hosu Kim
Created: 2025-03-19 16:27:08 UTC

Description:
    This module provides a FootballAPI class to interact with a football data API 
    to test the API connection and data retrieval.
'''

import requests
import json
from datetime import datetime, timedelta
import os
import sys
from typing import Dict, List, Optional, Any, Union

# Add parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import Settings

class FootballAPITester:
    """A tester class for the football API connection and data retrieval.

    Attributes:
        config (Settings): Configuration settings.
        base_url (str): base URL for API requests.
        headers (Dict[str, str]): HTTP headers for API authentication.
    """
    config: Settings
    base_url: str
    headers: Dict[str, str]

    def __init__(self, config: Settings) -> None:
        """Initialize the FootballAPITester.

        Args:
            config (Settings): Configuration settings object.
        """
        self.config = config
        self.base_url = self.config.api_football_url
        self.headers = {"x-apisports-key": self.config.api_football_key.get_secret_value()}

    def _call_api(self, endpoint_url: str, params: Optional[Dict[str, str]] = None) -> Optional[requests.Response]:
        """Interanl method to call the API.

        Args:
            endpoint_url (str): The full URL for the API endpoint.
            params (Optional[Dict[str, str]]): Query parameters for the API call.

        Returns:
            Optional[requests.Response]: The API response object or None if the request failed.
        """
        try:
            response: requests.Response = requests.get(
                endpoint_url,
                headers=self.headers,
                params=params
            )
            return response
        except requests.exceptions.RequestException as e:
            print(f"\nRequest Error: {str(e)}")
            return None

    def _print_response_details(self, response: Optional[requests.Response]) -> None:
        """Print details from an API response.
        
        Args:
            response (requests.Response): The API response object.
        """
        if response is None:
            return

        print(f"\nResponse Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")

        if response.status_code == 200:
            try:
                data: Dict[str, Any] = response.json()
                print("\nResponse Data Structure:")
                print(f"Keys in response: {list(data.keys())}")

                if 'response' in data:
                    matches: List[Dict[str, Any]] = data['response']
                    print(f"\nNumber of matches: {len(matches)}")

                    if matches:
                        print("\nFirst match details.")
                        print(json.dumps(matches[0], indent=2))
                    else:
                        print("No matches found for this date")

                if 'errors'in data:
                    print("\nAPI Errors:")
                    print(json.dumps(data['errors'], indent=2))
            except json.JSONDecodeError as e:
                print(f"\nJson Parsing Error: {str(e)}")

        else:
            print("\nError Response:")
            print(response.text)

    def test_fixtures_endpoint(self, date: Optional[str] = None) -> None:
        """Test the fixtures endpoing.
        
        Args:
            date (Optional[str]): Date string in YYYY-MM-DD format.
                                If not provided, yesterday's date is used.
        """
        if date is None:
            date = (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d")

        print(f"\n{'-'*60}")
        print(f"Testing Fixtures Endpoint")
        print(f"{'-'*60}")
        print(f"Current UTC Time: {datetime.utcnow().strftime('%Y-%m-%d %%H:%M:%S')}")
        print(f"Testing Date: {date}")

        endpoint_url = f"{self.base_url}/fixtures"
        params = {"date": date, "status": "FT-AET-PEN"}

        print(f"URL: {endpoint_url}")
        print(f"Parameters: {params}")

        response: Optional[requests.Response] = self._call_api(endpoint_url, params)
        self._print_response_details(response)

    def test_status_endpoint(self) -> None:
        """Test the status endpoint."""
        print(f"\n{'-'*60}")
        print(f"Testing Status Endpoint")
        print(f"{'-'*60}")

        endpoint_url = f"{self.base_url}/status"

        print(f"URL: {endpoint_url}")
        print(f"Parameters: {{}}")

        response: Optional[requests.Response] = self._call_api(endpoint_url)
        self._print_response_details(response)

    def test_api_connection(self) -> None:
        """Run all API connection tests."""
        print(f"\n{'='*60}")
        print("API Connection Test")
        print(f"{'='*60}")
        print(f"API URL Base: {self.base_url}")
        print(f"Headers: {self.headers}")

        # Test fixtures endpoint with yesterday's date
        self.test_fixtures_endpoint()

        # Test status endpoint
        self.test_status_endpoint()

def print_system_info() -> None:
    """Print system information for debugging."""
    print("\nStarting API test...")
    print(f"Current UTC Time: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Current working directory: {os.getcwd()}")
    print(f"Python path: {sys.path}")

if __name__ == "__main__":
    try:
        print_system_info()
        settings = Settings()
        tester = FootballAPITester(settings)
        tester.test_api_connection()
    except Exception as e:
        print(f"\nTest failed with error: {str(e)}")
