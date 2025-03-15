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
import logging
import sys
import os
import time  # Make sure this is imported at the top

# Add parent directory to path to ensure imports work correctly
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Always import from utils.config
from utils.config import setup_logger, load_config
from rich.console import Console

class FootballAPI:
    """Client for interacting with the football API."""

    def __init__(self):
        """Initialize the FootballAPI client."""
        config = load_config()
        self.api_key = config["football_api_key"]
        self.base_url = "https://api.football-data.org/v4"
        # Updated headers for football-data.org
        self.headers = {
            "X-Auth-Token": self.api_key,
        }

        # Use the unified logger
        self.logger = setup_logger("football_api")
        self.request_count = 0
        self.last_request_time = None

        self.console = Console()
        self.debug = True  # 디버그 출력 활성화 여부

        self.logger.info("FootballAPI initialized")

    def _rate_limit_check(self) -> bool:
        """Implement more robust API rate limiting.

        Ensures the API requests don't exceed rate limits by introducing
        delays when necessary.

        Returns:
            bool: True when the request can proceed.
        """
        now = datetime.datetime.now()

        # First request or more than 2 seconds since last request (increased from 1)
        if self.last_request_time is None or (now - self.last_request_time).total_seconds() >= 2:
            self.last_request_time = now
            self.request_count = 1
            return True

        # More conservative rate limit: maximum 5 requests per 10 seconds
        if self.request_count >= 5:
            wait_time = 3  # Increased wait time to 3 seconds
            if self.debug:
                self.console.print(f"[yellow]Rate limit reached, sleeping for {wait_time} seconds[/yellow]")
            self.logger.warning(f"Rate limit reached, sleeping for {wait_time} seconds")
            time.sleep(wait_time)
            self.last_request_time = datetime.datetime.now()
            self.request_count = 1
        else:
            self.request_count += 1
            # Add a small delay between all requests
            time.sleep(0.5)

        if self.debug:
            self.console.print(f"[dim]Rate limit check - Request count: {self.request_count}[/dim]")

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
        if self.debug:
            self.console.print(f"\n[yellow]Fetching matches for date: {date}[/yellow]")

        self.logger.info("Fetching matches for: %s", date)

        url = f"{self.base_url}/matches"
        params = {
            "dateFrom": date,
            "dateTo": date
        }

        # Add retry logic for handling rate limits
        max_retries = 3
        retry_count = 0
        retry_delay = 5  # Start with 5 seconds

        while retry_count < max_retries:
            try:
                self._rate_limit_check()
                if self.debug:
                    self.console.print(f"[blue]API Request:[/blue] {url}")
                    self.console.print(f"[blue]Params:[/blue] {params}")

                self.logger.info("Making API request to %s with params %s", url, params)
                response = requests.get(url, headers=self.headers, params=params)
                
                # Handle rate limiting with exponential backoff
                if response.status_code == 429:
                    retry_count += 1
                    if retry_count < max_retries:
                        wait_time = retry_delay * (2 ** (retry_count - 1))  # Exponential backoff
                        self.logger.warning(f"Rate limited (429). Retry {retry_count}/{max_retries} after {wait_time}s")
                        if self.debug:
                            self.console.print(f"[red]Rate limited (429). Retrying in {wait_time} seconds...[/red]")
                        time.sleep(wait_time)
                        continue
                
                response.raise_for_status()
                data = response.json()

                if self.debug:
                    self.console.print(f"[green]Response status: {response.status_code}[/green]")
                    self.console.print(f"[green]Found {len(data.get('matches', []))} fixtures[/green]")
                    # API 응답 데이터 출력 추가
                    self.console.print("\n[cyan]API Response Data:[/cyan]")
                    for match in data.get("matches", [])[:3]:  # 처음 3개 경기만 출력
                        self.console.print(
                            f"\n[yellow]Match:[/yellow] "
                            f"{match['homeTeam']['name']} vs {match['awayTeam']['name']}"
                        )
                        self.console.print(
                            f"[dim]League:[/dim] {match['competition']['name']}\n"
                            f"[dim]Score:[/dim] {match['score']['fullTime']['home']} - {match['score']['fullTime']['away']}\n"
                            f"[dim]Status:[/dim] {match['status']}\n"
                            f"[dim]Venue:[/dim] {match.get('venue', 'Unknown')}"
                        )
                    if len(data.get("matches", [])) > 3:
                        self.console.print("[dim]... and more matches ...[/dim]\n")

                self.logger.debug("API response received")

                matches = []
                for match in data.get("matches", []):
                    if match.get("status") in ["FINISHED", "AWARDED"]:
                        match_info = {
                            "date": date,
                            "home_team": match.get("homeTeam", {}).get("name", "Unknown"),
                            "away_team": match.get("awayTeam", {}).get("name", "Unknown"),
                            "home_score": match.get("score", {}).get("fullTime", {}).get("home", 0),
                            "away_score": match.get("score", {}).get("fullTime", {}).get("away", 0),
                            "league": match.get("competition", {}).get("name", "Unknown"),
                            "fixture_id": match.get("id"),
                            "goals": [],
                            "venue": match.get("venue", "Unknown"),
                            "match_time": match.get("utcDate", "Unknown"),
                            "events": []
                        }
                        matches.append(match_info)

                self.logger.info("Found %d completed matches for %s", len(matches), date)

                if self.debug:
                    self.console.print(f"[green]Successfully processed {len(matches)} completed matches[/green]")

                # Modify goal fetching to respect rate limits
                if matches and self.debug:
                    self.console.print("[yellow]Fetching goal details for matches...[/yellow]")

                if matches:
                    # Use single-threaded approach instead of ThreadPoolExecutor to better manage rate limits
                    match_goals = []
                    for match in matches:
                        goals = self._get_goals_for_match(match["fixture_id"])
                        match_goals.append(goals)
                        time.sleep(1)  # Add delay between goal fetches

                    # Assign goal data to matches
                    for i, match in enumerate(matches):
                        match["goals"] = match_goals[i]

                return matches
                
            except requests.exceptions.RequestException as e:
                retry_count += 1
                if response.status_code == 429 and retry_count < max_retries:
                    wait_time = retry_delay * (2 ** (retry_count - 1))  # Exponential backoff
                    self.logger.warning(f"Rate limited (429). Retry {retry_count}/{max_retries} after {wait_time}s")
                    if self.debug:
                        self.console.print(f"[red]Rate limited (429). Retrying in {wait_time} seconds...[/red]")
                    time.sleep(wait_time)
                else:
                    if self.debug:
                        self.console.print(f"[red]Error fetching matches:[/red] {str(e)}")
                    self.logger.error("Error fetching matches: %s", str(e), exc_info=True)
                    break  # Exit the retry loop on non-rate limit errors or max retries

        # Return empty list if all retries failed
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

    def _get_goals_for_match(self, match_id: int) -> List[Dict[str, Any]]:
        """Get goal details for a specific match with improved rate limiting.

        Args:
            match_id: The API's unique identifier for the match.

        Returns:
            A list of dictionaries containing goal data.
        """
        url = f"{self.base_url}/matches/{match_id}"
        
        # Add retry logic for handling rate limits
        max_retries = 3
        retry_count = 0
        retry_delay = 5  # Start with 5 seconds

        while retry_count < max_retries:
            try:
                self._rate_limit_check()
                if self.debug:
                    self.console.print(f"[dim]Fetching goals for match {match_id}...[/dim]")

                response = requests.get(url, headers=self.headers)
                
                # Handle rate limiting with exponential backoff
                if response.status_code == 429:
                    retry_count += 1
                    if retry_count < max_retries:
                        wait_time = retry_delay * (2 ** (retry_count - 1))  # Exponential backoff
                        self.logger.warning(f"Rate limited (429). Retry {retry_count}/{max_retries} after {wait_time}s")
                        if self.debug:
                            self.console.print(f"[red]Rate limited (429). Retrying in {wait_time} seconds...[/red]")
                        time.sleep(wait_time)
                        continue
                
                response.raise_for_status()
                data = response.json()

                goals = []
                for goal in data.get("goals", []):
                    scorer = goal.get("scorer", {}).get("name", "Unknown")
                    team_id = goal.get("team", {}).get("id")
                    minute = goal.get("minute")
                    
                    # Determine team name
                    team_name = None
                    if team_id == data.get("homeTeam", {}).get("id"):
                        team_name = data.get("homeTeam", {}).get("name")
                    else:
                        team_name = data.get("awayTeam", {}).get("name")
                    
                    goals.append({
                        "team": team_name,
                        "player": scorer,
                        "minute": minute,
                        "type": goal.get("type", "REGULAR")
                    })

                if self.debug and goals:
                    self.console.print(f"[dim]Found {len(goals)} goals for match {match_id}[/dim]")

                return goals
                
            except requests.exceptions.RequestException as e:
                retry_count += 1
                if response.status_code == 429 and retry_count < max_retries:
                    wait_time = retry_delay * (2 ** (retry_count - 1))  # Exponential backoff
                    self.logger.warning(f"Rate limited (429). Retry {retry_count}/{max_retries} after {wait_time}s")
                    if self.debug:
                        self.console.print(f"[red]Rate limited (429). Retrying in {wait_time} seconds...[/red]")
                    time.sleep(wait_time)
                else:
                    if self.debug:
                        self.console.print(f"[red]Error fetching goals for match {match_id}:[/red] {str(e)}")
                    self.logger.error("Error fetching goals for match %d: %s", match_id, str(e), exc_info=True)
                    break  # Exit the retry loop on non-rate limit errors or max retries

        # Return empty list if all retries failed
        return []

    def fetch_matches_by_date(self, date_str):
        """
        Fetch football matches for a specific date.
        
        Args:
            date_str (str): Date string in format 'YYYY-MM-DD'
            
        Returns:
            list: List of match dictionaries
        """
        self.logger.info(f"Fetching matches for date: {date_str}")
        return self.get_matches(date_str)

# Add this function to the module level (outside the FootballAPI class)
def fetch_matches_for_date(date_str):
    """
    Fetch football matches for a specific date.
    
    Args:
        date_str (str): Date string in format 'YYYY-MM-DD'
        
    Returns:
        list: List of match dictionaries
    """
    # Create a temporary instance of FootballAPI to use its methods
    api = FootballAPI()
    return api.fetch_matches_by_date(date_str)