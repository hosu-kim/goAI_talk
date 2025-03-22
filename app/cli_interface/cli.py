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
File: app/cli_interface/cli.py
Author: Hosu Kim
Created: 2025-03-15 20:01:20 UTC

Description:
    Command Line Interface for goAI_talk.
    Provides an interactive Q&A experience with rich text formatting and visual feedback.
'''

# Rich Library Imports for formatted console outputs
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
# Rich Library Imports for Prompt and Progress Indications
from rich.prompt import Prompt
from rich.progress import Progress, SpinnerColumn, TextColumn

from typing import List, Set, Optional, Union
from app.database_manager.database import Database
from datetime import datetime
from config import settings, Settings
from app.llm import QnAEngine
from app.domain.domain import Match

class CLI:
    """Command Line Interface for the goAI Talk application.

    This class handles the interactive command-line user interface,
    including user input, formatted output, and interaction with the QnA engine.
    """
    console: Console
    db: Database
    qna_engine: QnAEngine
    current_date: str
    match_data: Optional[List[Match]]

    def __init__(self, console: Console, db: Database, qna_engine: QnAEngine) -> None:
        """
        Initialize the CLI with injected dependencies.

        Args:
            console (console): An instance of the Rich Console for formatted output.
            db (Database): A pre-created Database instance.
            qna_engine (QnAEngine): A pre-created QnAEngine instance for generating answers.
        """
        self.console = console
        self.db = db
        self.qna_engine = qna_engine
        self.current_date = datetime.today().strftime("%Y-%m-%d")
        self.match_data = None

    def _load_match_data(self) -> None:
        """
        Load match data from database.
        """
        try:
            self.match_data = self.db.retrieve_yesterdays_matches_from_db()
        except Exception as e:
            self.console.print(f"[yellow]Warning: Could not load match data: {str(e)}[/yellow]")

    def display_welcome(self) -> None:
        """
        Display the welcome header and initial instructions.
        """
        header = (
            f"[bold cyan]goAI Talk[/bold cyan] - [yellow]Yesterday's Football Match Results Q&A Bot[/yellow]\n"
            f"[dim]Session: {self.current_date}[/dim]"
        )
        header_panel = Panel(Align.center(header), border_style="blue", padding=(1, 2))
        self.console.print(header_panel)
        self.console.print()

    def display_question_guide(self) -> None:
        """
        Display examples of questions that the user can ask.
        """
        guide_text = (
            "[bold cyan]Types of Questions You Can Ask:[/bold cyan]\n\n"
            "[bold yellow]Match Results[/bold yellow]\n"
            "  • [italic]What were yesterday's match results?[/italic]\n"
            "  • [italic]How many matches ended in a home win?[/italic]\n"
            "  • [italic]Which teams kept a clean sheet yesterday?[/italic]\n\n"
            "[bold yellow]Score Details[/bold yellow]\n"
            "  • [italic]Which match had the highest score?[/italic]\n"
            "  • [italic]What was the halftime score in the CSA match?[/italic]\n"
            "  • [italic]Were there any matches that went to extra time?[/italic]\n"
        )
        self.console.print(
            Panel(guide_text, title="[bold blue]Question Guide[/bold blue]", border_style="cyan", padding=(1, 2))
        )

    def display_data_context(self) -> None:
        """
        Display context information about the available match data.
        """
        leagues = self.get_leagues_from_data()
        leagues_list = "\n".join(f"  • {league}" for league in leagues[:10])
        if len(leagues) > 10:
            leagues_list += f"\n  • ...and {len(leagues) - 10} more leagues"
        match_date = "yesterday"
        if self.match_data and len(self.match_data) > 0:
            match_date = self.match_data[0].date
        match_count = len(self.match_data) if self.match_data else "Unknown"
        context = (
            f"[bold]Match Data:[/bold] {match_date}\n"
            f"[bold]Total Completed Matches:[/bold] {match_count}\n\n"
            f"[bold]Leagues Available:[/bold]\n{leagues_list}"
        )
        self.console.print(
            Panel(context, title="[bold blue]Available Data Context[/bold blue]", border_style="cyan", padding=(1 ,2))
        )

    def get_leagues_from_data(self) -> List[str]:
        """
        Extract the unique league names from match data.

        Returns:
            List[str]: A sorted list of league names.
        """
        if not self.match_data:
            return ["(Data not available)"]
        leagues = {f"{match.league} ({getattr(match, 'country', 'Unknown')})" for match in self.match_data if match.league}
        return sorted(list(leagues))

    def process_user_input(self) -> str:
        """
        Prompt and return user input.

        Returns:
            str: The input question from the user.
        """
        return Prompt.ask("\n[bold green]Question[/bold green]")

    def display_answer(self, answer: str) -> None:
        """
        Display the given answer in a formatted panel.

        Args:
            answer (str): The answer to display.
        """
        self.console.print(
            Panel(Text(answer, style="bright_white"), title="[bold blue]Answer[/bold blue]", border_style="cyan", padding=(1, 2))
        )

    def run(self) -> None:
        """
        Entry-point method to run the CLI interface.
        This method calls several helper methods to perform its tasks.
        """
        self._load_match_data()
        self.display_welcome()
        self.display_question_guide()
        while True:
            self.run_once()
            self.console.print("\n" + "=" * self.console.width + "\n")

    def run_once(self) -> None:
        """
        Process a single user input and display a response.
        This abstracts part of the run loop for clarity.
        """
        question = self.process_user_input()
        if question.lower() in ['exit', 'quit']:
            self.console.print(
                Panel("[yellow]Thanks for using goAI Talk! See you next time![/yellow]", border_style="cyan", padding=(1, 2))
            )
            exit(0)
        elif question.lower() in ['help', '?', 'examples']:
            self.display_question_guide()
        elif question.lower() in ['info', 'data', 'context']:
            self.display_data_context()
        else:
            try:
                with Progress(SpinnerColumn(), TextColumn("[bold blue]Thinking...[/bold blue]"), transient=True) as progress:
                    progress.add_task("generating", total=None)
                    answer = self.qna_engine.get_answer(question)
                self.display_answer(answer)
            except Exception as e:
                self.console.print(
                    Panel(f"[bold red]Error:[/bold red] {str(e)}", border_style="red", padding=(1, 2))
                )
