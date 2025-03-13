import requests
import datetime
import os
import json
from dotenv import load_dotenv

load_dotenv()

class FootballAPI:
	def __init__(self):
		self.api_key = os.getenv("FOOTBALL_API_KEY")
		self.base_url = "https://v3.football.api-sports.io"
		self.headers = {
			"x-apisports-key": self.api_key,
		}

	def get_matches(self, date):
		"""Get matches for a specific date"""
		print(f"Fetching matches for: {date}")

		url = f"{self.base_url}/fixtures"
		params = {"date": date}

		try:
			response = requests.get(url, headers=self.headers, params=params)
			response.raise_for_status()
			data = response.json()
			print("API 응답 내용:") # de
			print(json.dumps(data, indent=2, ensure_ascii=False)) #de

			if "response" not in data:
				print("Unexpected API response format")
				return []

			matches = []
			for fixture in data["response"]:
				if fixture["status"]["short"] == "FT":
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

			for match in matches:
				match["goals"] = self._get_goals_for_match(match["fixture_id"])

			return matches
		
		except Exception as e:
			print(f"Error fetching matches: {e}")
			return []
			

	def get_yesterdays_matches(self):
		yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
		return self.get_matches(yesterday)
		
	def fetch_yesterday_matches(self, db_manager):
		matches = self.get_yesterdays_matches()
		if matches:
			db_manager.save_matches(matches)
			print(f"Saved {len(matches)} matches to the database")
		return matches
	
	def _get_goals_for_match(self, fixture_id):
		url = f"{self.base_url}/fixtures/events"
		params = {"fixture": fixture_id}

		try:
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

			return goals
		except Exception as e:
			print(f"Error fetching goals for match {fixture_id}: {e}")
			return []