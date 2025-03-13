"""
CLI interface for the Football Matches Q&A Bot.

This module provides a command-line interface for interacting with
the football question-answering systen. Users can query information
about recent football matches through a text-based interface.
"""

import argparse
import sys
import time
from datetime import datetime, timedelta
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table

from api.football_api import FootballAPI
from database.database_manager import DBManager
from llm.qna_engine import QnAEngine

class FootballQnACLI:
	"""command-line interface for the Football Q&A system."""

	def __init__(self, football_api, db_manager, qna_engine):
		"""
		Initialize the CLI appliation with required components.
		Sets up the console, database, API, and QnA engine.
		"""
		self.console = Console()

		self.db_manager = db_manager
		self.football_api = football_api
		self.qna_engine = qna_engine

		self.data_refreshed = False

	def start(self):
		"""
		Start the CLI application.
		Display welcome message and enter the main loop.
		"""
		self._display_header()

		try:
			self._check_data_freshness()
			self._main_loop()
		except KeyboardInterrupt:
			self.console.print("\n[yellow]Program terminated by user.[/yellow]")
		except Exception as e:
			self.console.print(f"[bold red]Error: {str(e)}[/bold red]")
		finally:
			self.console.print("[green]Thanks for using Football Q&A bot! Goodbye![/green]")

	def _display_header(self):
		"""Display the application header and info."""
		self.console.print(Panel.fit(
			"[bold green]Football Matches Q&A Bot[/bold green]\n"
			"[italic]Ask me anything about recent football matches![/italic]",
			border_style="green"
		))

		current_time = datetime.utcnow()
		self.console.print(f"[dim]Current Date and Time (UTC): {current_time.strftime('%Y-%m-%d %H:%M:%S')}[/dim]")

		self.console.print(f"\ntype [bold]'help'[/bold] for available commands or [bold]'exit'[/bold] to quit.\n")

	def _check_data_freshness(self):
		"""Check if match data nedds to be refreshed from API."""
		last_update = self.db_manager.get_last_update_time()
		current_time = datetime.utcnow()

		if not last_update or current_time - last_update > timedelta(hours=12):
			self.console.print("[yellow]Match data is outdated. Refreshing from API...[/yellow]")
			self._refresh_data()
		else:
			self.console.print(f"[dim]Using cached match data (last updated: {last_update.strftime('%Y-%m-%d %H:%M:%S')} UTC)[/dim]")

	def _refresh_data(self):
		"""Refresh match data from the football API."""
		with self.console.status("[bold green]Fetching latest match data...[/bold green]"):
			try:
				yesterday = datetime.utcnow() - timedelta(days=1)
				date_str = yesterday.strftime("%Y-%m-%d")

				matches = self.football_api.get_matches(date_str)

				self.db_manager.save_matches(matches)
				self.data_refreshed = True

				self.console.print(f"[green]Successfully refreshed data. {len(matches)} matches retrieved.[/green]")
			except Exception as e:
				self.console.print(f"[bold red]Failed to refresh data: {str(e)}[/bold red]")
	
	def _main_loop(self):
		"""Main interaction loop for handling user input."""
		while True:
			user_input = Prompt.ask("\n[bold cyan]Ask me about football matches[/bold cyan]")
			user_input = user_input.strip().lower()

			if user_input in ("exit", "quit", "q"):
				break
			elif user_input == "help":
				self._show_help()
			elif user_input in ("refresh", "update"):
				self._refresh_data()
			elif user_input in ("leagues", "competitions"):
				self._show_available_leagues()
			elif user_input == "teams":
				self._show_available_teams()
			elif user_input == "matches":
				self._show_matches_summary()
			# Handle questions
			elif user_input:
				self._process_question(user_input)

	def _process_question(self, question):
		"""
		Process a user's question and display the answer.

		Args:
			question (str): User's football-related question
		"""
		self.console.print("[dim]Thinking...[/dim]")

		yesterday = datetime.utcnow() - timedelta(days=1)
		date_str = yesterday.strftime("%Y-%m-%d")
		matches = self.db_manager.get_matches(date_str)

		if not matches:
			self.console.print("[yellow]No match data available for yesterday.[/yellow]")
			return

		try:
			# Get answer from QnA engine
			with self.console.status("[bold green]Generating answer...[/bold green]"):
				answer = self.qna_engine.get_answer(question, matches)

			# Display answer in a panel
			self.console.print(Panel(
				answer, 
				title="[bold]Answer[/bold]",
				border_style="blue"
			))
		except Exception as e:
			self.console.print(f"[bold red]Error generating answer: {str(e)}[/bold red]")

	def _show_help(self):
		"""Display help information with available commands."""
		help_table = Table(title="Available Commands.")
		help_table.add_column("Command", style="cyan")
		help_table.add_column("Description")

		help_table.add_row("help", "Show this help message")
		help_table.add_row("exit, quit, q", "Exit the application")
		help_table.add_row("refresh, update", "Refresh match data from API")
		help_table.add_row("leagues, competitions", "Show available leagues")
		help_table.add_row("teams", "Show available teams")
		help_table.add_row("matches", "Show summary of yesterday's matches")
		help_table.add_row("<question>", "Ask any question about yesterday's matches")

		self.console.print(help_table)

		self.console.print("\n[italic]Example questions:[/italic]")
		self.console.print("  • Who won the Premeier League match yesterday?")
		self.console.print("  • Did Manchester United play yesterday?")
		self.console.print("  • How many goals were scored in La Liga?")
		self.console.print("  • Who scored for Arsenal?")

	def _show_available_leagues(self):
		"""Display a list of leagues with matches in the database."""
		yesterday = datetime.utcnow() - timedelta(days=1)
		date_str = yesterday.strftime("%Y-%m-%d")
		leagues = self.db_manager.get_leagues(date_str)

		if not leagues:
			self.console.print("[yellow]No league data available.[/yellow]")
			return
		
		leagues_table = Table(title="Available Leagues")
		leagues_table.add_column("League", style="cyan")
		leagues_table.add_column("Matches", justify="right")

		for league in leagues:
			leagues_table.add_row(league["name"], str(league["match_count"]))
		
		self.console.print(leagues_table)

	def _show_available_teams(self):
		"""display a list of teams that played in yesterday's matches."""
		yesterday = datetime.utcnow() - timedelta(days=1)
		date_str = yesterday.strftime("%Y-%m-%d")
		teams = self.db_manager.get_teams(date_str)

		if not teams:
			self.console.print("[yellow]No team data available.[/yellow]")
			return
		
		teams_table = Table(title="Teams That Played Yesterday")
		teams_table.add_column("Team", style="cyan")
		teams_table.add_column("League", style="green")

		for team in teams:
			teams_table.add_row(team["name"], team["league"])

		self.console.print(teams_table)

	def _show_matches_summary(self):
		"""Display a summary of yesterday's matches."""
		yesterday = datetime.utcnow() - timedelta(days=1)
		date_str = yesterday.strftime("%Y-%m-%d")
		matches = self.db_manager.get_matches(date_str)

		if not matches:
			self.console.print("[yellow]No match data available for yesterday.[/yellow]")
			return
		
		matches_table = Table(title=f"Matches Summary ({date_str})")
		matches_table.add_column("League", style="green")
		matches_table.add_column("Home", style="cyan")
		matches_table.add_column("Score", style="bold")
		matches_table.add_column("Away", style="cyan")

		for match in matches:
			matches_table.add_row(
				match["league"],
				match["home_team"],
				f"{match['home_score']} - {match['away_score']}",
				match["away_team"]
			)

		self.console.print(matches_table)

	def main():
		"""Entry point for the CLI application."""
		parser = argparse.ArgumentParser(description="Foolball Maches Q&A CLI")
		parser.add_argument("--refresh", action="store_true", help="Force refresh of match data")
		args = parser.parse_args()

		cli = FootballQnACLI()

		if args.refresh:
			cli.console.print("[yellow]forcing data refresh...[/yellow]")
			cli._refresh_data()

		cli.start()

	if __name__ == "__main__":
		main()