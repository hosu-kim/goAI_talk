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
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any
from config import Settings
from .domain.domain import Match
from .models import RawAPIResponse
from .exceptions import APIConnectionError, APIResponseError, DataProcessingError

# Get a logger for this module
logger = logging.getLogger(__name__)

class FootballAPI:
    """A client for interacting with the football data API.
    
    This class provides methods to fetch and process football match data
    from an external API service.
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
        logger.info(f"FootballAPI initialized with use_test_date={use_test_data}")

    def get_yesterdays_matches(self) -> List[Match]:
        """Retrieves football matches from yesterday.

        Fetches data either from the API or from test data based on configuration.

        Returns:
            List[Match]: A list of match objects containing match information.

        Raises:
            APIConnectionError: If there's an error connecting to the API.
            APIResponseError: If the API returns an unexpected response.
            DataProcessingError: If there's an error processing the API data.
        """
        if self.use_test_data:
            logger.info("Using test data instead of API-Football api")
            return self._load_test_data()

        yesterday: str = (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d")
        endpoint: str = f"{self.config.api_football_url}/fixtures"
        params: Dict[str, str] = {
            "date": yesterday,
            "status": "FT-AET-PEN"
        }

        logger.info(f"Fetching matches for {yesterday} from API")
        logger.debug(f"API endpoint: {endpoint}")
        logger.debug(f"API parameters: {params}")

        try:
            response: requests.Response = requests.get(
                endpoint,
                headers=self.headers,
                params=params
            )
            logger.debug(f"API Response Status: {response.status_code}")

            if response.status_code != 200:
                error_msg = f"API Error: {response.text}"
                logger.error(error_msg)
                raise APIResponseError(error_msg)

            data = response.json()
            matches = self._process_api_response(data)
            logger.info(f"Successfully retrieved {len(matches)} matches")
            return matches

        except requests.RequestException as e:
            error_msg = f"API request failed: {str(e)}"
            logger.error(error_msg, exc_info=True)
            raise APIConnectionError(error_msg)
        except Exception as e:
            error_msg = f"Error processing match data: {str(e)}"
            logger.error(error_msg, exc_info=True)
            raise DataProcessingError(error_msg)
    

    """=========================== TEST DATA LOAD ==========================="""
    def _load_test_data(self) -> List[Match]:
        """Loads match data from a local test file for development purposes.

        Returns:
            List[Match]: A list of Match objects containing processed match data.

        Raises:
            DataProcessingError: If there's an error loading or processing the test data.
        """
        try:
            logger.info("Loading test data from tests/test_data.json")
            with open('tests/test_data.json', 'r') as file:
                test_data = json.load(file)
            matches = self._process_api_response(test_data)
            logger.info(f"Successfully loaded {len(matches)} matches from test data")
            return matches
        except (FileNotFoundError, json.JSONDecodeError) as e:
            error_msg = f"Error loading test data: {str(e)}"
            logger.error(error_msg, exc_info=True)
            raise DataProcessingError(error_msg)

    def _process_api_response(self, data: List[Dict[str, Any]]) -> List[Match]:
        """"Process the API response using Pydantic models for validation.

        Args:
            data (Dict[str, Any]): The raw API response data.

        Returns:
            List[Match]: A list of validated Match domain objects.

        Raises:
            DataProcessingError: If the data does not match the expected structure.
        """
        try:
            logger.debug("Processing API response data")
            if 'response' not in data:
                error_msg = "Unexpected API response format: 'response' key missing"
                logger.error(error_msg)
                raise APIResponseError(error_msg)

            json_data = json.dumps(data)

            logger.debug("validating response format with Pydantic model")
            validated_response = RawAPIResponse.model_validate_json(json_data)

            matches = [
                raw_match.to_match_model().to_domain()
                for raw_match in validated_response.response
            ]

            logger.debug(f"Processed {len(matches)} matches from API response")
            return matches

        except Exception as e:
            error_msg = f"Error processing API data: {str(e)}"
            logger.error(error_msg, exc_info=True)
            raise DataProcessingError(error_msg)
