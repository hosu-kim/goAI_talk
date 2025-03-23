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
File: app/database.py
Author: Hosu Kim
Created: 2025-03-15 19:02:33 UTC

Description: 
    This module handles SQLite database operations for storing
    and retrieving football match data including scores, teams, and goal details.
'''

import sqlite3
import json
import logging
from typing import List, Dict, Any, Optional
from config import Settings
from app.domain.domain import Match, GoalEvent

# Get a logger for this module
logger = logging.getLogger(__name__)

class Database:
    """A class to handle all database operations for football match data.

    This class provides methods to create tables, save match data and retrieve
    match information from a SQLite database.
    It supports both production and test environments.

    Attributes:
        db_path (str): Path to the SQLite database file.
        use_test_data (bool): Flag to indicate if test data should be used.
    """
    db_path: str
    use_test_data: bool

    def __init__(self, config: Settings, use_test_data: bool =False) -> None:
        """Initialize the Database instance.

        Args:
            config (Settings): Application configuration settings.
            use_test_data (bool, optional): Whether to use test data mode.
                                            Defaults to False.
        """

        self.db_path = config.db_path
        self.use_test_data = use_test_data
        logger.info(f"Database initialized with path: {self.db_path}")
        self._create_tables()

    def _create_tables(self) -> None:
        """Create necessary database tables if they don't exist.

        Creates a 'matches' table with the following columns:
            - match_id (PRIMARY KEY): Unique identifier for each match
            - date: Date of the match
            - league: Name of the league/competition
            - country: Country where the match was played
            - home_team: Name of the home team
            - away_team: Name of the away team
            - home_score: Goals scored by home team
            - away_score: Goals scored by away team
            - goals: JSON string containing goal details
        """
        logger.debug("Creating database tables if they don't exist")
        conn = sqlite3.connect(self.db_path)
        cursor: sqlite3.Cursor = conn.cursor()

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS matches (
            match_id INTEGER PRIMARY KEY,
            date TEXT,
            league TEXT,
            country TEXT,
            home_team TEXT,
            away_team TEXT,
            home_score INTEGER,
            away_score INTEGER,
            goals TEXT
        )
        ''')

        conn.commit()
        conn.close()
        logger.debug("Database tables created/verified successfully")

    def save_matches(self, matches: List[Match]) -> None:
        """Save or update match data in the database.

        Args:
            matches (list): List of dictionaries containing match information.
                            Each object must provide the necessary attributes.
        Note:
            Uses INSERT OR REPLACE to handle both new entries and updates.
            Goal information is stored as a JSON string in the database.
        """
        logger.info(f"Saving {len(matches)} matches to database")
        conn: sqlite3.Connection = sqlite3.connect(self.db_path)
        cursor: sqlite3.Cursor = conn.cursor()

        for match in matches:
            # Prepare a dictionary from the Match object; if your Match class doesn't have
            # a conversion method, you might convert the dataclass to dict using asdict(match).
            match_dict = {
                "match_id": match.match_id,
                "date": match.date,
                "league": match.league,
                "country": getattr(match, "country", ""), # Ensure to handle field accordingly.
                "home_team": match.home_team,
                "away_team": match.away_team,
                "home_score": match.home_score,
                "away_score": match.away_score,
                "goals": json.dumps([goal.__dict__ for goal in match.goal_events])
            }

            logger.debug(f"Saving match {match.match_id}: {match.home_team} vs {match.away_team}")
            cursor.execute('''
            INSERT OR REPLACE INTO matches
            (match_id, date, league, country, home_team, away_team, home_score, away_score, goals)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                match_dict['match_id'],
                match_dict['date'],
                match_dict['league'],
                match_dict['country'],
                match_dict['home_team'],
                match_dict['away_team'],
                match_dict['home_score'],
                match_dict['away_score'],
                match_dict['goals'],
            ))

        conn.commit()
        conn.close()
        logger.info("Matches saved successfully")

    def retrieve_yesterdays_matches_from_db(self, max_matches: Optional[int] = None) -> List[Match]:
        """Retrieve yesterday's match data from database.

        Fetches matches from the most recent retrieved_date in the database.
        Goal information is automatically parsed from JSON back into Python objects.

        Args:
           max_matches (Optional[int]): Maximum number of matches to return.
                                      If None, returns all matches.

        Returns:
            List[Match]: List of Match objects containing match details including
            scores, teams, and goal events. Returns empty list if
            no matches found or on database error.
        Raises:
            sqlite3.Error: If there's an error accessing the database.
        """
        logger.info(f"Retrieving matches from database (max_matches={max_matches})")
        conn: Optional[sqlite3.Connection] = None
        matches: List[Match] = []
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row  # Enable row factory for dict-like access
            cursor: sqlite3.Cursor = conn.cursor()

            # Query with optional limit
            if max_matches:
                logger.debug(f"Limiting query to {max_matches} matches")
                cursor.execute('SELECT * FROM matches LIMIT ?', (max_matches,))
            else:
                cursor.execute('SELECT * FROM matches')

            for row in cursor.fetchall():
                row_dict: Dict[str, Any] = dict(row)
                # Parse JSON goals string back to list of dictionaries
                if row_dict.get('goals'):
                    goals_data = json.loads(row_dict['goals'])
                else:
                    goals_data = []

                # Covert each goal dict into a GoalEvent object
                # Assuming the keys in goals_data match the GoalEvent dataclass
                goal_events = [GoalEvent(**goal) for goal in goals_data]

                match = Match(
                    match_id=row_dict['match_id'],
                    date=row_dict['date'],
                    league=row_dict['league'],
                    country=row_dict['country'],
                    home_team=row_dict['home_team'],
                    away_team=row_dict['away_team'],
                    home_score=row_dict['home_score'],
                    away_score=row_dict['away_score'],
                    goal_events=goal_events
                )

                matches.append(match)

            logger.info(f"Retrieved {len(matches)} matches from database")
            return matches
        except sqlite3.Error as e:
            error_msg = f"Database error: {e}"
            logger.error(error_msg, exc_info=True)
            return []
        finally:
            if conn:
                conn.close()
