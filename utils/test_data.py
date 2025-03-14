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
File: utils/test_data.py
Author: hosu-kim
Created: 2025-03-15

Description:
    This module provides mock football match data for testing and development.
    It eliminates the need for API calls during development and testing.
"""
from datetime import datetime, timedelta
import logging

# Set up logger
logger = logging.getLogger("test_data")

def get_yesterday_date():
    """Get yesterday's date in YYYY-MM-DD format."""
    yesterday = datetime.now() - timedelta(days=1)
    return yesterday.strftime("%Y-%m-%d")

def get_test_matches(date=None):
    """
    Get sample football match data for testing.
    
    Args:
        date (str, optional): Date in YYYY-MM-DD format. Defaults to yesterday.
        
    Returns:
        list: List of match dictionaries containing sample data
    """
    if date is None:
        date = get_yesterday_date()
    
    logger.info(f"Generating test match data for {date}")
    
    # Sample match data reflecting common football league matches
    test_matches = [
        # Premier League matches
        {
            "date": date,
            "home_team": "Manchester United",
            "away_team": "Liverpool",
            "home_score": 2,
            "away_score": 1,
            "league": "Premier League",
            "fixture_id": 1001,
            "venue": "Old Trafford",
            "match_time": f"{date}T15:00:00+00:00",
            "goals": [
                {"team": "Manchester United", "player": "Bruno Fernandes", "minute": 24, "type": "Normal Goal"},
                {"team": "Liverpool", "player": "Mohamed Salah", "minute": 55, "type": "Normal Goal"},
                {"team": "Manchester United", "player": "Marcus Rashford", "minute": 78, "type": "Normal Goal"}
            ]
        },
        {
            "date": date,
            "home_team": "Arsenal",
            "away_team": "Chelsea",
            "home_score": 3,
            "away_score": 0,
            "league": "Premier League",
            "fixture_id": 1002,
            "venue": "Emirates Stadium",
            "match_time": f"{date}T17:30:00+00:00",
            "goals": [
                {"team": "Arsenal", "player": "Martin Odegaard", "minute": 15, "type": "Normal Goal"},
                {"team": "Arsenal", "player": "Bukayo Saka", "minute": 35, "type": "Penalty"},
                {"team": "Arsenal", "player": "Gabriel Jesus", "minute": 67, "type": "Normal Goal"}
            ]
        },
        {
            "date": date,
            "home_team": "Manchester City",
            "away_team": "Tottenham",
            "home_score": 4,
            "away_score": 2,
            "league": "Premier League",
            "fixture_id": 1003,
            "venue": "Etihad Stadium",
            "match_time": f"{date}T20:00:00+00:00",
            "goals": [
                {"team": "Manchester City", "player": "Erling Haaland", "minute": 8, "type": "Normal Goal"},
                {"team": "Manchester City", "player": "Kevin De Bruyne", "minute": 23, "type": "Normal Goal"},
                {"team": "Tottenham", "player": "Son Heung-min", "minute": 40, "type": "Normal Goal"},
                {"team": "Manchester City", "player": "Erling Haaland", "minute": 51, "type": "Normal Goal"},
                {"team": "Tottenham", "player": "Richarlison", "minute": 72, "type": "Normal Goal"},
                {"team": "Manchester City", "player": "Phil Foden", "minute": 85, "type": "Normal Goal"}
            ]
        },
        
        # La Liga matches
        {
            "date": date,
            "home_team": "Barcelona",
            "away_team": "Real Madrid",
            "home_score": 2,
            "away_score": 2,
            "league": "La Liga",
            "fixture_id": 2001,
            "venue": "Camp Nou",
            "match_time": f"{date}T20:00:00+00:00",
            "goals": [
                {"team": "Barcelona", "player": "Robert Lewandowski", "minute": 22, "type": "Normal Goal"},
                {"team": "Real Madrid", "player": "Vinicius Junior", "minute": 35, "type": "Normal Goal"},
                {"team": "Barcelona", "player": "Raphinha", "minute": 60, "type": "Normal Goal"},
                {"team": "Real Madrid", "player": "Jude Bellingham", "minute": 90, "type": "Normal Goal"}
            ]
        },
        {
            "date": date,
            "home_team": "Atletico Madrid",
            "away_team": "Sevilla",
            "home_score": 1,
            "away_score": 0,
            "league": "La Liga",
            "fixture_id": 2002,
            "venue": "Wanda Metropolitano",
            "match_time": f"{date}T18:30:00+00:00",
            "goals": [
                {"team": "Atletico Madrid", "player": "Antoine Griezmann", "minute": 54, "type": "Normal Goal"}
            ]
        },
        
        # Serie A matches
        {
            "date": date,
            "home_team": "Juventus",
            "away_team": "Inter",
            "home_score": 1,
            "away_score": 1,
            "league": "Serie A",
            "fixture_id": 3001,
            "venue": "Allianz Stadium",
            "match_time": f"{date}T19:45:00+00:00",
            "goals": [
                {"team": "Juventus", "player": "Dusan Vlahovic", "minute": 33, "type": "Normal Goal"},
                {"team": "Inter", "player": "Lautaro Martinez", "minute": 65, "type": "Normal Goal"}
            ]
        },
        {
            "date": date,
            "home_team": "AC Milan",
            "away_team": "Napoli",
            "home_score": 2,
            "away_score": 0,
            "league": "Serie A",
            "fixture_id": 3002,
            "venue": "San Siro",
            "match_time": f"{date}T17:00:00+00:00",
            "goals": [
                {"team": "AC Milan", "player": "Rafael Leao", "minute": 28, "type": "Normal Goal"},
                {"team": "AC Milan", "player": "Olivier Giroud", "minute": 76, "type": "Penalty"}
            ]
        },
        
        # Bundesliga matches
        {
            "date": date,
            "home_team": "Bayern Munich",
            "away_team": "Borussia Dortmund",
            "home_score": 3,
            "away_score": 2,
            "league": "Bundesliga",
            "fixture_id": 4001,
            "venue": "Allianz Arena",
            "match_time": f"{date}T17:30:00+00:00",
            "goals": [
                {"team": "Bayern Munich", "player": "Harry Kane", "minute": 12, "type": "Normal Goal"},
                {"team": "Borussia Dortmund", "player": "Julian Brandt", "minute": 24, "type": "Normal Goal"},
                {"team": "Bayern Munich", "player": "Leroy Sané", "minute": 45, "type": "Normal Goal"},
                {"team": "Borussia Dortmund", "player": "Marco Reus", "minute": 67, "type": "Normal Goal"},
                {"team": "Bayern Munich", "player": "Jamal Musiala", "minute": 82, "type": "Normal Goal"}
            ]
        },
        
        # Ligue 1 matches
        {
            "date": date,
            "home_team": "PSG",
            "away_team": "Marseille",
            "home_score": 3,
            "away_score": 1,
            "league": "Ligue 1",
            "fixture_id": 5001,
            "venue": "Parc des Princes",
            "match_time": f"{date}T19:45:00+00:00",
            "goals": [
                {"team": "PSG", "player": "Kylian Mbappé", "minute": 10, "type": "Normal Goal"},
                {"team": "PSG", "player": "Ousmane Dembélé", "minute": 25, "type": "Normal Goal"},
                {"team": "Marseille", "player": "Pierre-Emerick Aubameyang", "minute": 55, "type": "Normal Goal"},
                {"team": "PSG", "player": "Kylian Mbappé", "minute": 70, "type": "Penalty"}
            ]
        },
        
        # K League matches (for Korean market)
        {
            "date": date,
            "home_team": "Jeonbuk Hyundai Motors",
            "away_team": "FC Seoul",
            "home_score": 2,
            "away_score": 1,
            "league": "K League 1",
            "fixture_id": 6001,
            "venue": "Jeonju World Cup Stadium",
            "match_time": f"{date}T09:00:00+00:00",
            "goals": [
                {"team": "Jeonbuk Hyundai Motors", "player": "Gustavo", "minute": 34, "type": "Normal Goal"},
                {"team": "FC Seoul", "player": "Ki Sung-yueng", "minute": 50, "type": "Penalty"},
                {"team": "Jeonbuk Hyundai Motors", "player": "Kim Jin-su", "minute": 88, "type": "Normal Goal"}
            ]
        },
        {
            "date": date,
            "home_team": "Ulsan Hyundai",
            "away_team": "Pohang Steelers",
            "home_score": 3,
            "away_score": 0,
            "league": "K League 1",
            "fixture_id": 6002,
            "venue": "Ulsan Munsu Football Stadium",
            "match_time": f"{date}T11:30:00+00:00",
            "goals": [
                {"team": "Ulsan Hyundai", "player": "Joo Min-kyu", "minute": 14, "type": "Normal Goal"},
                {"team": "Ulsan Hyundai", "player": "Um Won-sang", "minute": 45, "type": "Normal Goal"},
                {"team": "Ulsan Hyundai", "player": "Lee Chung-yong", "minute": 77, "type": "Normal Goal"}
            ]
        }
    ]
    
    logger.info(f"Generated {len(test_matches)} test matches")
    return test_matches

def get_test_leagues(date=None):
    """
    Get sample leagues from test match data.
    
    Args:
        date (str, optional): Date in YYYY-MM-DD format. Defaults to yesterday.
        
    Returns:
        list: List of league dictionaries with name and match count
    """
    if date is None:
        date = get_yesterday_date()
    
    matches = get_test_matches(date)
    leagues = {}
    
    for match in matches:
        league_name = match["league"]
        if league_name in leagues:
            leagues[league_name] += 1
        else:
            leagues[league_name] = 1
    
    return [{"name": name, "match_count": count} for name, count in leagues.items()]

def get_test_teams(date=None):
    """
    Get sample teams from test match data.
    
    Args:
        date (str, optional): Date in YYYY-MM-DD format. Defaults to yesterday.
        
    Returns:
        list: List of team dictionaries with name and league
    """
    if date is None:
        date = get_yesterday_date()
    
    matches = get_test_matches(date)
    teams = []
    team_names = set()
    
    for match in matches:
        home_team = match["home_team"]
        away_team = match["away_team"]
        league = match["league"]
        
        if home_team not in team_names:
            team_names.add(home_team)
            teams.append({"name": home_team, "league": league})
            
        if away_team not in team_names:
            team_names.add(away_team)
            teams.append({"name": away_team, "league": league})
    
    return teams

class TestFootballAPI:
    """Mock Football API that returns test data."""
    
    def __init__(self):
        """Initialize the test football API."""
        self.logger = logging.getLogger("test_football_api")
        self.logger.info("Initialized TestFootballAPI")
    
    def get_matches(self, date, location=None):
        """
        Get test matches for a specific date.
        
        Args:
            date (str): The date in YYYY-MM-DD format.
            location (str, optional): Optional user location for filtering.
            
        Returns:
            list: Test match data.
        """
        matches = get_test_matches(date)
        
        # Filter by location if provided
        if location and location.lower() in ["korea", "seoul", "south korea"]:
            self.logger.info(f"Filtering matches for Korean user: {location}")
            # Prioritize K League matches and add them first
            korean_matches = [m for m in matches if m["league"] == "K League 1"]
            other_matches = [m for m in matches if m["league"] != "K League 1"]
            return korean_matches + other_matches[:8]  # Limit to avoid overwhelming
            
        return matches
    
    def get_yesterdays_matches(self):
        """Get test matches for yesterday's date."""
        yesterday = get_yesterday_date()
        self.logger.info(f"Getting test matches for yesterday: {yesterday}")
        return get_test_matches(yesterday)
        
    def fetch_yesterday_matches(self, db_manager):
        """
        Fetch test match data for yesterday and save to database.
        
        Args:
            db_manager: Database manager to save matches.
            
        Returns:
            list: Test match data
        """
        matches = self.get_yesterdays_matches()
        if matches and db_manager:
            self.logger.info(f"Saving {len(matches)} test matches to database")
            db_manager.save_matches(matches)
        return matches

class TestDBManager:
    """Mock Database Manager that stores test data in memory."""
    
    def __init__(self):
        """Initialize the test database manager."""
        self.logger = logging.getLogger("test_db_manager")
        self.matches = {}  # Store matches by date
        self.last_updated = None
        self.logger.info("Initialized TestDBManager")
    
    def save_matches(self, matches):
        """
        Save matches to in-memory storage.
        
        Args:
            matches (list): List of match dictionaries.
            
        Returns:
            bool: True if successful.
        """
        if not matches:
            return False
            
        date = matches[0]["date"]
        self.matches[date] = matches
        self.last_updated = datetime.now()
        self.logger.info(f"Saved {len(matches)} matches for {date}")
        return True
    
    def get_matches(self, date=None):
        """
        Retrieve matches from in-memory storage.
        
        Args:
            date (str, optional): Date to retrieve matches for.
            
        Returns:
            list: List of match dictionaries.
        """
        if date is None:
            # Return all matches
            all_matches = []
            for date_matches in self.matches.values():
                all_matches.extend(date_matches)
            return all_matches
            
        return self.matches.get(date, [])
    
    def get_leagues(self, date=None):
        """Get leagues from test data."""
        return get_test_leagues(date)
    
    def get_teams(self, date=None):
        """Get teams from test data."""
        return get_test_teams(date)
    
    def get_last_update_time(self):
        """Get the last update time."""
        return self.last_updated
