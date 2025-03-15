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
File: database/database_manager.py
Author: hosu-kim
Created: 2025-03-14 10:45:18 UTC

Description:
    This module provides database management functionality.
    It handles storing and retrieving football match data from SQLite database.
"""
import sqlite3
import os
import logging
from datetime import datetime
from contextlib import contextmanager
from typing import Generator, List, Dict, Any

# Import the unified logger setup from utils
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.config import setup_logger

class DBManager:
    def __init__(self):
        """Initialize database manager with updated paths."""
        self.db_dir = "database"
        os.makedirs(self.db_dir, exist_ok=True)
        self.db_path = os.path.join(self.db_dir, "football_matches.db")
        
        # Use the unified logger setup
        self.logger = setup_logger("database")
        self.logger.info("Database Manager initialized")

        self._setup_database()
    
    # Remove the setup_logger method as we're now using the unified one
    
    def _setup_database(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        self.logger.info("Setting up database tables")

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS matches (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        home_team TEXT,
        away_team TEXT,
        home_score INTEGER,
        away_score INTEGER,
        league TEXT,
        fixture_id INTEGER,
        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS goals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        match_id INTEGER,
        team TEXT,
        player TEXT,
        minute INTEGER,
        FOREIGN KEY (match_id) REFERENCES matches (id)
        )
        ''')

        conn.commit()
        conn.close()
        self.logger.info(f"Database setup complete at {self.db_path}")

    @contextmanager
    def get_connection(self) -> Generator:
        """Context manager for database connections."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise
        finally:
            conn.close()
            
    def save_matches(self, matches: List[Dict[str, Any]]) -> bool:
        """Save match data to database with improved error handling."""
        if not matches:
            self.logger.warning("No matches to save.")
            return False
            
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                for match in matches:
                    cursor.execute('''
                    INSERT INTO MATCHES (date, home_team, away_team, home_score, away_score, league, fixture_id)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        match["date"],
                        match["home_team"],
                        match["away_team"],
                        match["home_score"],
                        match["away_score"],
                        match["league"],
                        match["fixture_id"]
                    ))

                    match_id = cursor.lastrowid
                    self.logger.debug(f"Inserted match: {match['home_team']} vs {match['away_team']} with ID {match_id}")

                    for goal in match.get("goals", []):
                        cursor.execute('''
                        INSERT INTO goals (match_id, team, player, minute)
                        VALUES (?, ?, ?, ?)
                        ''', (
                            match_id,
                            goal["team"],
                            goal["player"],
                            goal["minute"]
                        ))

            self.logger.info(f"Successfully saved {len(matches)} matches to database.")
            return True
        
        except sqlite3.IntegrityError as e:
            self.logger.error(f"Database integrity error: {e}")
            return False
        except Exception as e:
            self.logger.error(f"Unexpected error saving matches: {e}")
            return False
    
    def _clear_old_data(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            self.logger.info("Clearing old data from database")
            cursor.execute("DELETE FROM goals")
            cursor.execute("DELETE FROM matches")
            conn.commit()
        except Exception as e:
            conn.rollback()
            self.logger.error(f"Error clearing old data: {e}", exc_info=True)
        finally:
            conn.close()
    
    def get_matches(self, date=None):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        try:
            query = '''
            SELECT id, date, home_team, away_team, home_score, away_score, league, fixture_id
            FROM matches
            '''
            params = []
            
            if date:
                query += " WHERE date = ?"
                params.append(date)
                
            cursor.execute(query, params)
            self.logger.info(f"Retrieving matches" + (f" for date: {date}" if date else ""))

            matches = []
            for match_row in cursor.fetchall():
                match = dict(match_row)
                match_id = match["id"]

                cursor.execute('''
                SELECT team, player, minute
                FROM goals
                WHERE match_id = ?
                ORDER BY minute
                ''', (match_id,))

                match["goals"] = [dict(goal) for goal in cursor.fetchall()]
                matches.append(match)

            self.logger.info(f"Retrieved {len(matches)} matches")
            return matches
            
        except Exception as e:
            self.logger.error(f"Error retrieving matches from database: {e}", exc_info=True)
            return []
        
        finally:
            conn.close()

    def get_leagues(self, date=None):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        try:
            query = "SELECT league, COUNT(*) as match_count FROM matches"
            params = []

            if date:
                query += " WHERE date = ?"
                params.append(date)

            query += " GROUP BY league ORDER BY match_count DESC"
            
            self.logger.info(f"Retrieving leagues" + (f" for date: {date}" if date else ""))
            cursor.execute(query, params)

            leagues = []
            for row in cursor.fetchall():
                leagues.append({"name": row["league"], "match_count": row["match_count"]})

            self.logger.info(f"Retrieved {len(leagues)} leagues")
            return leagues
        except Exception as e:
            self.logger.error(f"Error getting leagues: {e}", exc_info=True)
            return []
        finally:
            conn.close()

    def get_teams(self, date=None):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        try:
            self.logger.info(f"Retrieving teams" + (f" for date: {date}" if date else ""))
            teams = []

            # Get home teams
            query_home = """
            SELECT home_team as name, league FROM matches
            """
            params = []

            if date:
                query_home += " WHERE date = ?"
                params.append(date)

            cursor.execute(query_home, params)
            for row in cursor.fetchall():
                teams.append(dict(row))
            
            # Get away teams
            query_away = """
            SELECT away_team as name, league FROM matches
            """
            params = []

            if date:
                query_away += " WHERE date = ?"
                params.append(date)

            cursor.execute(query_away, params)
            for row in cursor.fetchall():
                teams.append(dict(row))

            unique_teams = []
            team_names = set()

            for team in teams:
                if team["name"] not in team_names:
                    team_names.add(team["name"])
                    unique_teams.append(team)

            self.logger.info(f"Retrieved {len(unique_teams)} unique teams")
            return unique_teams
        except Exception as e:
            self.logger.error(f"Error getting teams: {e}", exc_info=True)
            return []
        finally:
            conn.close()

    def get_last_update_time(self):
        """get the timestamp of the last database update"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            self.logger.debug("Checking last database update time")
            cursor.execute("SELECT MAX(last_updated) FROM matches")
            last_update_str = cursor.fetchone()[0]

            if last_update_str:
                update_time = datetime.fromisoformat(last_update_str)
                self.logger.info(f"Last database update: {update_time}")
                return update_time
            
            self.logger.info("No previous database updates found")
            return None
        except Exception as e:
            self.logger.error(f"Error getting last update time: {e}", exc_info=True)
            return None
        finally:
            conn.close()
