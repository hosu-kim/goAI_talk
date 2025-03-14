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
File: api/football_api.py
Author: hosu-kim
Created: 2025-03-14 11:11:38 UTC

Description:
    This module provides the FootballAPI class to interact with the football data API,
    fetching matches, goals, and related information.
"""
import requests
import datetime
import concurrent.futures
from typing import List, Dict, Any, Optional
from utils.config import setup_logger, load_config

class FootballAPI:
    """Client for interacting with the football API.

    This class handles API requests to fetch football match data, goals,
    and other related information.
    """

    def __init__(self):
        """Initialize the FootballAPI client.

        Loads API key and sets up headers, base URL, and logger.
        """
        config = load_config()
        self.api_key = config["football_api_key"]
        self.base_url = "https://v3.football.api-sports.io"
        self.headers = {
            "x-apisports-key": self.api_key,
        }

        self.logger = setup_logger("football_api")
        self.request_count = 0
        self.last_request_time = None

        self.logger.info("FootballAPI initialized")

    def _rate_limit_check(self) -> bool:
        """Implement API rate limiting.

        Ensures the API requests don't exceed rate limits by introducing
        delays when necessary.

        Returns:
            bool: True when the request can proceed.
        """
        now = datetime.datetime.now()

        # First request or more than 1 second since last request
        if self.last_request_time is None or (now - self.last_request_time).total_seconds() >= 1:
            self.last_request_time = now
            self.request_count = 1
            return True

        # Limit to maximum 10 requests per second
        if self.request_count >= 10:
            self.logger.warning("Rate limit reached, sleeping for 1 second")
            import time
            time.sleep(1)
            self.last_request_time = datetime.datetime.now()
            self.request_count = 1
        else:
            self.request_count += 1

        return True

    def get_matches(self, date: str) -> List[Dict[str, Any]]:
        """Get matches for a specific date.

        Args:
            date: The date in YYYY-MM-DD format.

        Returns:
            A list of dictionaries containing match data.

        Raises:
            Exception: If the API request fails.
        """
        self.logger.info("Fetching matches for: %s", date)

        url = f"{self.base_url}/fixtures"
        params = {"date": date}

        try:
            self._rate_limit_check()
            self.logger.info("Making API request to %s with params %s", url, params)
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()

            self.logger.debug("API response received")

            if "response" not in data:
                self.logger.error("Unexpected API response format")
                return []

            matches = []
            for fixture in data["response"]:
                if fixture["fixture"]["status"]["short"] == "FT":
                    match = {
                        "date": date,
                        "home_team": fixture["teams"]["home"]["name"],
                        "away_team": fixture["teams"]["away"]["name"],
                        "home_score": fixture["goals"]["home"],
                        "away_score": fixture["goals"]["away"],
                        "league": fixture["league"]["name"],
                        "fixture_id": fixture["fixture"]["id"],
                        "goals": [],
                        "venue": fixture["fixture"].get("venue", {}).get("name", "Unknown"),
                        "match_time": fixture["fixture"].get("date", "Unknown"),
                        "events": []
                    }
                    matches.append(match)

            self.logger.info("Found %d completed matches for %s", len(matches), date)

            # Get goal data in parallel for better performance
            if matches:
                with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
                    match_goals = list(executor.map(
                        self._get_goals_for_match, 
                        [match["fixture_id"] for match in matches]
                    ))

                # Assign goal data to matches
                for i, match in enumerate(matches):
                    match["goals"] = match_goals[i]

            return matches

        except Exception as e:
            self.logger.error("Error fetching matches: %s", str(e), exc_info=True)
            return []

    def get_matches_by_team(self, team_name: str, date: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get matches for a specific team.

        Args:
            team_name: The name of the team to search for.
            date: Optional date in YYYY-MM-DD format. 
                  Defaults to yesterday if not provided.

        Returns:
            A list of dictionaries containing match data for the team.
        """
        try:
            if date is None:
                # Default to yesterday
                date = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")

            matches = self.get_matches(date)
            team_matches = []

            for match in matches:
                if team_name.lower() in match["home_team"].lower() or team_name.lower() in match["away_team"].lower():
                    team_matches.append(match)

            self.logger.info("Found %d matches for team '%s' on %s", len(team_matches), team_name, date)
            return team_matches

        except Exception as e:
            self.logger.error("Error fetching matches for team %s: %s", team_name, str(e), exc_info=True)
            return []

    def get_yesterdays_matches(self) -> List[Dict[str, Any]]:
        """Get matches for yesterday's date.

        Returns:
            A list of dictionaries containing match data.
        """
        yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        self.logger.info("Getting matches for yesterday: %s", yesterday)
        return self.get_matches(yesterday)

    def fetch_yesterday_matches(self, db_manager) -> List[Dict[str, Any]]:
        """Fetch yesterday's matches and save to database.

        Args:
            db_manager: Database manager instance to save matches.

        Returns:
            A list of dictionaries containing match data.
        """
        self.logger.info("Fetching yesterday's matches and saving to database")
        matches = self.get_yesterdays_matches()
        if matches:
            db_manager.save_matches(matches)
            self.logger.info("Saved %d matches to the database", len(matches))
        return matches

    def _get_goals_for_match(self, fixture_id: int) -> List[Dict[str, Any]]:
        """Get goal details for a specific match.

        Args:
            fixture_id: The API's unique identifier for the fixture.

        Returns:
            A list of dictionaries containing goal data.
        """
        url = f"{self.base_url}/fixtures/events"
        params = {"fixture": fixture_id}

        try:
            self._rate_limit_check()
            self.logger.debug("Fetching goals for fixture: %d", fixture_id)
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()

            goals = []
            for event in data["response"]:
                if event["type"] == "Goal" and event["detail"] != "Missed Penalty":
                    goal = {
                        "team": event["team"]["name"],
                        "player": event["player"]["name"],
                        "minute": event["time"]["elapsed"],
                        "type": event.get("detail", "Goal")
                    }
                    goals.append(goal)

            self.logger.debug("Found %d goals for fixture %d", len(goals), fixture_id)
            return goals
        except Exception as e:
            self.logger.error("Error fetching goals for match %d: %s", fixture_id, str(e), exc_info=True)
            return []