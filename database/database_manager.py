import sqlite3
import os
import json
from datetime import datetime

class DBManager:
	def __init__(self):
		self.db_dir = "database"
		os.makedirs(self.db_dir, exist_ok=True)
		self.db_path = os.path.join(self.db_dir, "football_matches.db")
		self._setup_database()

	def _setup_database(self):
		conn = sqlite3.connect(self.db_path)
		cursor = conn.cursor()

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
		scorer TEXT,
		minute INTEGER,
		FOREIGN KEY (match_id) REFERENCES matches (id)
		)
		''')

		conn.commit()
		conn.close()
		print(f"Database setup complete at {self.db_path}")

	def save_matches(self, matches):
		if not matches:
			print("No matches to save.")
			return False
		
		self._clear_old_data()

		conn = sqlite3.connect(self.db_path)
		cursor = conn.cursor()

		try:
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

				for goal in match.get("goals", []):
					cursor.execute('''
					INSERT INTO goals (match_id, team, scorer, minute)
					VALUES (?, ?, ?, ?)
					''', (
						match_id,
						goal["team"],
						goal["scorer"],
						goal["minute"]
					))

			conn.commit()
			print(f"Successfully saved {len(matches)} matches to database.")
			return True
		
		except Exception as e:
			conn.rollback()
			print(f"Error saving matches to database: {e}")
			return False
		
		finally:
			conn.close()
	
	def _clear_old_data(self):
		conn = sqlite3.connect(self.db_path)
		cursor = conn.cursor()

		try:
			cursor.execute("DELETE FROM goals")
			cursor.execute("DELETE FROM matches")
			conn.commit()
		except Exception as e:
			conn.rollback()
			print(f"Error clearing old data: {e}")
		finally:
			conn.close()
	
	def get_matches(self, date=None):
		conn = sqlite3.connect(self.db_path)
		conn.row_factory = sqlite3.Row
		cursor = conn.cursor()

		try:
			cursor.execute('''
			SELECT id, date, home_team, away_team, home_score, away_score, league, fixture_id
			FROM matches
			''')

			matches = []
			for match_row in cursor.fetchall():
				match = dict(match_row)
				match_id = match["id"]

				cursor.execute('''
				SELECT team, scorer,minute
				FROM goals
				WHERE match_id = ?
				ORDER BY minute
				''', (match_id,))

				match["goals"] = [dict(goal) for goal in cursor.fetchall()]
				matches.append(match)

			return matches
			
		except Exception as e:
			print(f"Error retrieving matches from database: {e}")
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
				query += " Where date = ?"
				params.append(date)

			query += " GROUP BY league ORDER BY match_count DESC"

			cursor.execute(query, params)

			leagues = []
			for row in cursor.fetchall():
				leagues.append({"name": row["league"], "match_count": row["match_count"]})

			return (leagues)
		except Exception as e:
			print(f"Error getting leagues: {e}")
			return []
		finally:
			conn.close()

	def get_teams(self, date=None):
		conn = sqlite3.connect(self.db_path)
		conn.row_factory = sqlite3.Row
		cursor = conn.cursor()

		try:
			teams = []

			# Get home teams
			query_home = """
			SELECT home_team as name, league FROM  matches
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

			# Remove duplicates (teams might play multiple matches)
			unique_teams = []
			team_names = set()

			for team in teams:
				if team["name"] not in team_names:
					team_names.add(team["name"])
					unique_teams.append(team)

			return unique_teams
		except Exception as e:
			print(f"Error getting teams: {e}")
			return []
		finally:
			conn.close()

	def get_last_update_time(self):
		"""get the timestamp of the last database update"""
		conn = sqlite3.connect(self.db_path)
		cursor = conn.cursor()

		try:
			cursor.execute("SELECT MAX(last_updated) FROM matches")
			last_update_str = cursor.fetchone()[0]

			if last_update_str:
				return datetime.fromisoformat(last_update_str)
			return None
		except Exception as e:
			print(f"Error getting last update time: {e}")
			return None
		finally:
			conn.close()