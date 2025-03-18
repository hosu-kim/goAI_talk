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


class Database:
    """A class to handle all database operations for football match data.

    This class provides methods to create tables, save match data, and retrieve
    match information from a SQLite database. It supports both production and
    test environments.

    Attributes:
        db_path (str): Path to the SQLite database file.
        use_test_data (bool): Flag to indicate if test data should be used.
    """
    def __init__(self, db_path="app/database_manager/football_data.db", use_test_data=False):
        """Initialize the Database instance.

        Args:
            db_path (str, optional): Path to the SQLite database file.
                                   Defaults to "football_data.db".
            use_test_data (bool, optional): Whether to use test data mode.
                                          Defaults to False.
        """

        self.db_path = db_path
        
        self.use_test_data = use_test_data
        self._create_tables()

    def _create_tables(self):
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
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

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

    def save_matches(self, matches):
        """Save or update match data in the database.

        Args:
            matches (list): List of dictionaries containing match information.
                          Each dictionary should contain:
                          - match_id: Unique identifier
                          - date: Match date
                          - league: League name
                          - country: Country name
                          - home_team: Home team name
                          - away_team: Away team name
                          - goals: List of goal events (will be converted to JSON)

        Note:
            Uses INSERT OR REPLACE to handle both new entries and updates.
            Goal information is stored as a JSON string in the database.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        for match in matches:
            # Convert goals list to JSON string for storage
            goals_json = json.dumps(match.get('goals', []))

            # Insert or update match data
            cursor.execute('''
            INSERT OR REPLACE INTO matches
            (match_id, date, league, country, home_team, away_team, home_score, away_score, goals)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                match['match_id'],
                match['date'],
                match['league'],
                match['country'],
                match['home_team'],
                match['away_team'],
                match['home_score'],
                match['away_score'],
                goals_json,
            ))

        conn.commit()
        conn.close()

    def get_yesterdays_matches_from_db(self, max_matches=None):
        """Retrieve yesterday's match data from database.

        Fetches matches from the most recent retrieved_date in the database.
        Goal information is automatically parsed from JSON back into Python objects.

        Args:
           max_matches (int, optional): Maximum number of matches to return.
                                      If None, returns all matches.

        Returns:
            list: List of dictionaries containing match information.
                Each dictionary contains all match details with goals parsed
                from JSON.

        Raises:
            sqlite3.Error: If there's an error accessing the database.
                         Error is logged and empty list is returned.
        """
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row  # Enable row factory for dict-like access
            cursor = conn.cursor()

            # Query with optional limit
            if max_matches:
                cursor.execute('SELECT * FROM matches LIMIT ?', (max_matches,))
            else:
                cursor.execute('SELECT * FROM matches')

            # Process results and parse JSON goals data
            matches = []
            for row in cursor.fetchall():
                match = dict(row)
                # Convert JSON goals string back to Python object
                if match['goals']:
                    match['goals'] = json.loads(match['goals'])
                matches.append(match)

            return matches
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return []
        finally:
            if conn:
                conn.close()
