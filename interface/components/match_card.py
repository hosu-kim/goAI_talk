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
File: interface/components/match_card.py
Author: hosu-kim
Created: 2024-03-14

Description:
    This module provides functionality to create match result cards
    showing scores, teams, and goal details using Rich library components.
"""
from rich.panel import Panel
from rich.text import Text
from rich.table import Table

def create_match_card(match, console):
    """Creates a visual card representation of a football match result.
    
    Generates a formatted panel showing match details including teams,
    scores, and goal information with appropriate styling.
    
    Args:
        match (dict): Match information containing:
            - home_team (str): Name of home team
            - away_team (str): Name of away team
            - home_score (int): Home team score
            - away_score (int): Away team score
            - league (str): League name
            - date (str): Match date
            - goals (list, optional): List of goal information
        console (Console): Rich console object for display
        
    Returns:
        Panel: A Rich Panel object containing the formatted match information
    """
    # Set team names and scores
    home_team = match["home_team"]
    away_team = match["away_team"]
    home_score = match["home_score"]
    away_score = match["away_score"]
    
    # Display winner color
    home_style = "bold green" if home_score > away_score else "white"
    away_style = "bold green" if away_score > home_score else "white"
    
    if home_score == away_score:
        home_style = away_style = "yellow"
    
    # Compose title
    title = Text()
    title.append(f"{match['league']} ", style="blue")
    title.append(f"({match['date']})")
    
    # Match information table
    match_table = Table(show_header=False, box=None)
    match_table.add_column("Team", style="cyan")
    match_table.add_column("Score", justify="center", style="bold")
    
    # Add team information
    match_table.add_row(Text(home_team, style=home_style), f"{home_score}")
    match_table.add_row(Text(away_team, style=away_style), f"{away_score}")
    
    # Add goal information if available
    content = [match_table]
    
    if match.get("goals") and len(match["goals"]) > 0:
        goals_text = Text("\nGoals:\n", style="italic")
        
        for goal in match["goals"]:
            scorer = goal["player"]
            team = goal["team"]
            minute = goal["minute"]
            goals_text.append(f"⚽ {minute}' {scorer} ({team})\n")
        
        content.append(goals_text)
    
    return Panel(
        "\n".join(str(item) for item in content),
        title=title,
        border_style="green" if len(match.get("goals", [])) > 0 else "blue"
    )
