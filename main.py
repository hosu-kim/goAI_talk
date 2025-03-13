import argparse
from api.football_api import FootballAPI
from database.database_manager import DBManager
from llm.qna_engine import QnAEngine
from interface.cli import FootballQnACLI
import os
from dotenv import load_dotenv

load_dotenv()

def main():
	parser = argparse.ArgumentParser(description="Football Match Results Q&A Bot")
	parser.add_argument("--fetch", action="store_true", help="Fetch yesterday's match data")
	parser.add_argument("--web", action="store_true", help="Run web interface instead of CLI")
	args = parser.parse_args()

	football_api = FootballAPI()
	data_manager = DBManager()
	qna_engine = QnAEngine()

	# Check if fetch flag is set
	if args.fetch:
		print("Fetching yesterday's match data...")
		football_api.fetch_yesterday_matches(data_manager)

	# Determine which interface to run
	if args.web:
		# Import web interface module only when needed
		from interface.web import run_web_app
		print("Starting web interface...")
		run_web_app(data_manager, qna_engine)
	else:
		# Start CLI interface
		print("Starting CLI interface...")
		cli = FootballQnACLI(football_api, data_manager, qna_engine)
		cli.start()

if __name__ == "__main__":
	main()
