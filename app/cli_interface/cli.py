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

goAI_talk - Yesterday's Football Match Results Q&A Bot
File: app/cli_interface/cli.py
Author: Hosu Kim
Created: 2025-03-15 20:01:20 UTC

Description:
    Command Line Interface for goAI_talk.
    Provides an interactive Q&A experience with rich text formatting and visual feedback.
'''

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.align import Align
from app.llm import QnAEngine
from app.database_manager.database import Database
from datetime import datetime

class CLI:
    """Command Line Interface for the goAI Talk application.
    
    This class handles the interactive command-line user interface,
    including user input, formatted output, and interaction with the QnA engine.
    
    Attributes:
        qna_engine: An istance of QnAEngine for processing questions.
        console: Rich Console instance for forammted terminal output.
        current_date: Current date string in YYYY-MM-DD format.
        db: Datebase instance for accessing match data.
        match_data: Cached match data from the database.
    """
    def __init__(self):
        """Initialize the CLI with required components and load match data."""
        self.qna_engine = QnAEngine()
        self.console = Console()
        self.current_date = datetime.today().strftime("%Y-%m-%d")
        self.db = Database()
        self.match_data = None
        self._load_match_data()
        
    def _load_match_data(self):
        """Load match data from database to get context information.
        
           If an error occurs during data loading, a warning is displayed.
        """
        try:
            self.match_data = self.db.get_yesterdays_matches_from_db()
            # Status will always be "Match Finished" for all matches
        except Exception as e:
            self.console.print(f"[yellow]Warning: Could not load match data: {str(e)}[/yellow]")
        
    def _get_leagues_from_data(self):
        """Extract unique leagues from match data.
        
           Returns:
               list: Sorted list of league names with countries, or a placeholder if no data.
        """
        if not self.match_data:
            return ["(Data not available)"]
        
        leagues = set()
        for match in self.match_data:
            if 'league' in match and match['league']:
                leagues.add(f"{match['league']} ({match['country']})")
        
        return sorted(list(leagues))
        
    def _get_header(self):
        """Get formatted header with current tim
           Returns:
               str: Rich text formatted header for display.
        """
        header = (
            f"[bold cyan]goAI Talk[/bold cyan] - [yellow]Yesterday's Football Match Results Q&A Bot[/yellow]\n"
            f"[dim]Session: {self.current_date}[/dim]"
        )
        return header

    def _display_welcome(self):
        """Display welcome message with styled header.

           Shows information about the application and available commands.
        """
        # Create header panel
        header_panel = Panel(
            Align.center(self._get_header()),
            border_style="blue",
            padding=(1, 2)
        )
        
        # Get match date from data if available
        match_date = "yesterday's completed matches"
        if self.match_data and len(self.match_data) > 0 and 'date' in self.match_data[0]:
            match_date = f"completed matches from {self.match_data[0]['date']}"
        
        # Create welcome message panel
        welcome_panel = Panel(
            f"[dim]Welcome to goAI Talk! Ask me anything about {match_date}.\n"
            "Type [bold]'help'[/bold] to see example questions, [bold]'info'[/bold] for data context, "
            "or [bold]'exit'[/bold]/[bold]'quit'[/bold] to end the session.[/dim]",
            border_style="cyan",
            padding=(1, 2)
        )
        
        self.console.print(header_panel)
        self.console.print(welcome_panel)
        self.console.print()  # Empty line for spacing

    def _display_question_guide(self):
        """Display examples of questions users can ask about football matches/

           Organizes example questions by category in a formatted panel.
        """
        categories = {
                "Match Results": [
                    "What were yesterday's match results?",
                    "How many matches ended in a home win?",
                    "Which teams kept a clean sheet yesterday?"
                ],
                "Score Details": [
                    "Which match had the highest score?",
                    "What was the halftime score in the CSA match?",
                    "Were there any matches that went to extra time or penalties?"
                ],
                "League Information": [
                    "Show me all CONCACAF Champions League matches",
                    "What matches were played in the Copa Do Brasil?",
                    "How many different leagues had matches yesterday?"
                ],
                "Venue & Location": [
                    "Which matches were played in Brazil?",
                    "What matches were played at Independence Park?",
                    "Show me all match venues and their cities"
                ],
                "Team Performance": [
                    "Did Inter Miami win their match?",
                    "Which team scored the most goals in a single match?",
                    "Show me all matches where the home team won"
                ]
            }
        
        content = "[bold cyan]Types of Questions You Can Ask:[/bold cyan]\n\n"
        
        for category, questions in categories.items():
            content += f"[bold yellow]{category}[/bold yellow]\n"
            for q in questions:
                content += f"  • [italic]{q}[/italic]\n"
            content += "\n"
        
        content += "[dim]Type 'help' anytime to see this guide again.[/dim]"
        
        self.console.print(Panel(
            content,
            title="[bold blue]Question Guide[/bold blue]",
            border_style="cyan",
            padding=(1, 2)
        ))

    def _display_data_context(self):
        """Display information about the available data the bot can answer about.

           Shows match date, total matches, available leagues, and date types.
        """
        leagues = self._get_leagues_from_data()
        leagues_list = "\n".join([f"  • {league}" for league in leagues[:10]])
        if len(leagues) > 10:
            leagues_list += f"\n  • ...and {len(leagues) - 10} more leagues"
        
        # Get match date from data if available
        match_date = "yesterday"
        if self.match_data and len(self.match_data) > 0 and 'date' in self.match_data[0]:
            match_date = self.match_data[0]['date']
            
        match_count = len(self.match_data) if self.match_data else "Unknown"
        
        context = (
            f"[bold]Match Data:[/bold] {match_date}\n"
            f"[bold]Total Completed Matches:[/bold] {match_count}\n\n"
            f"[bold]Leagues Available:[/bold]\n"
            f"{leagues_list}\n\n"
            f"[bold]Data Includes:[/bold]\n"
            f"  • Match dates, leagues, and countries\n"
            f"  • Team information (home and away)\n"
            f"  • Full-time and half-time scores\n"
            f"  • Goal details and match statistics\n"
            f"  • Match venues and locations\n"
            f"  • All matches have 'Match Finished' status\n"
        )
        
        self.console.print(Panel(
            context,
            title="[bold blue]Available Data Context[/bold blue]",
            border_style="cyan",
            padding=(1, 2)
        ))

    def _get_user_input(self):
        """Get styled user input/

        Returns:
            str: User's question or command.
        """
        return Prompt.ask("\n[bold green]Question[/bold green]")

    def _display_answer(self, answer):
        """Display styled answer in a panel.

           Args:
               Answer (str): The answer text to display.
        """
        self.console.print(Panel(
            Text(answer, style="bright_white"),
            title="[bold blue]Answer[/bold blue]",
            border_style="cyan",
            padding=(1, 2)
        ))

    def _format_error(self, message):
        """Format error messages.

           Args:
               message (str): The error message to format.

           Returns:
               Panel: A formatted error panel.
        """
        return Panel(
            f"[bold red]Error:[/bold red] {message}",
            border_style="red",
            padding=(1, 2)
        )

    def run(self):
        """Run the CLI interface with rich formatting.

           Main loop that handles user interaction, command processing,
           and displays formatted responses.
        """
        # Clear screen and display welcome message
        self.console.clear()
        self._display_welcome()
        
        # Show question guide on first run
        self._display_question_guide()

        while True:
            # Get user input
            question = self._get_user_input()
            
            # Check for special commands
            if question.lower() in ['exit', 'quit']:
                self.console.print(
                    Panel(
                        "[yellow]Thanks for using goAI Talk! See you next time![/yellow]",
                        border_style="cyan",
                        padding=(1, 2)
                    )
                )
                break
            elif question.lower() in ['help', '?', 'examples']:
                self._display_question_guide()
                continue
            elif question.lower() in ['info', 'data', 'context']:
                self._display_data_context()
                continue

            # Show progress while generating answer
            try:
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[bold blue]Thinking...[/bold blue]"),
                    transient=True
                ) as progress:
                    progress.add_task("generating", total=None)
                    answer = self.qna_engine.get_answer(question)

                # Display the answer
                self._display_answer(answer)
            except Exception as e:
                # Handle any errors that might occur
                self.console.print(self._format_error(f"Failed to generate answer: {str(e)}"))
            
            # Add a separator line
            self.console.print("\n" + "═" * self.console.width + "\n")

def main():
    """Main entry point for the CLI application.

       Initializes and runs the CLI, handling any uncaught exceptions.
    """
    cli = CLI()
    try:
        cli.run()
    except KeyboardInterrupt:
        cli.console.print("\n[yellow]Program interrupted. Exiting...[/yellow]")
    except Exception as e:
        cli.console.print(f"\n[bold red]An unexpected error occurred:[/bold red] {str(e)}")

if __name__ == "__main__":
    main()
