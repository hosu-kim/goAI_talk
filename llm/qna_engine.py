import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class QnAEngine:
	"""
		QnA Engine for processing football-related questions using LLM.
		This class handles the integration with OpenAI's API to generate
		natural language response based on provided match data.
		
	"""
	def __init__(self):
		"""
		Initialize the QnA Engine with OpenAI client.
		Sets up the API connection using the API key from environment variables.
		"""
		api_key=os.getenv("OPENAI_API_KEY")
		if not api_key:
			raise ValueError("OPENAI_API_KEY not found in environment variables")

		os.environ["OPENAI_API_KEY"] = api_key
		self.client = None

	def get_answer(self, question, matches):
		"""
		Generate an answer for a football-related question based on match data.
		
		Args:
			question (str): User's question about football matches
			matches (list): List of match data objects containing game information

		Returns:
			str: LLM-generated response to the user's question
		"""
		try:
			from openai import OpenAI
			client = OpenAI()

			matches_data = self._format_matches_data(matches)
			prompt = f"""
			You are an AI assistant answering questions about recent football match results.
			Please provide accurate answers based on the football match data provided below. ;)

			Yesterday's football match data:
			{matches_data}

			Question: {question}

			Guidelines:
			1. Only use information from the provided data.
			2. If information is not in the data, state that you don't know.
			3. Use precise team names, player names, and scores.
			4. Answer in the same language as the question.
			"""

			response = client.chat.completions.create(
				model="gpt-4",
				messages=[
					{"role": "system", "content": "You are a helpful football results assistant."},
					{"role": "user", "content": prompt}
				]
			)

			return response.choices[0].message.content
		
		except Exception as e:
			print(f"Error getting answer from LLM: {e}")
			return "Sorry, an error occurred while answering your question."
		
	def _format_matches_data(self, matches):
		"""
		Format match data into a structured string for LLM processing.
		
		Args:
			matches (list): List of match data objects
			
		Returns:
			str: Formatted string representation of match data
		"""
		formatted_data = []

		for match in matches:
			match_info = f"""
			Match: {match["home_team"]} vs {match["away_team"]}
			Score: {match["home_score"]} - {match["away_score"]}
			Time: {match["match_time"]}
			League: {match["league"]}
			Venue: {match["venue"]}

			Goals:
			{self._format_goals(match["goals"])}

			Key Events:
			{self._format_events(match["events"])}
			"""
			formatted_data.append(match_info)

		return "\n---\n".join(formatted_data)

	def _format_goals(self, goals):
		"""
		Format goal information into a readable string.
		
		Args:
			goals (list): List of goal events
			
		Returns:
			str: Formatted string of goal information
		"""
		if not goals:
			return "No goals"
		
		goal_strings = []
		for goal in goals:
			goal_str = f"- {goal['minute']}: {goal['player']} ({goal['team']}) {goal['type']}"
			goal_strings.append(goal_str)

		return "\n".join(goal_strings)
	
	def _format_events(self, events):
		"""
		Format match events (cards, substitutions, etc.) into a readable string.
		
		Args:
			events (list): List of match events
		
		Returns:
			str: Formatted string of match events
		"""
		if not events:
			return "No significant events"
		
		event_strings = []
		for event in events:
			event_str = f"- {event.get('minute')}': {event.get('type')} - {event.get('player')} ({event.get('team')})"
			event_strings.append(event_str)

		return "\n".join(event_strings)