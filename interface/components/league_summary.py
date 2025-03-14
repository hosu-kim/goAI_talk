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
File: interface/components/league_summary.py
Author: hosu-kim
Created: 2024-03-14

Description:
    This module provides functionality to generate league summaries 
    and scoring statistics using Rich library components.
    Includes league tables and goal scoring summaries.
"""
from rich.table import Table
from rich.text import Text

def create_league_summary(leagues, console):
    """Creates a summary table for all football leagues.
    
    Args:
        leagues (list): List of league information dictionaries containing:
            - name (str): League name
            - match_count (int): Number of matches in the league
        console (Console): Rich console object for display
        
    Returns:
        Table: A Rich Table object showing league names and their match counts
    """
    table = Table(title="Football Leagues", show_lines=False)
    
    table.add_column("League", style="cyan")
    table.add_column("Matches", style="green", justify="right")
    
    for league in sorted(leagues, key=lambda x: x["match_count"], reverse=True):
        table.add_row(league["name"], str(league["match_count"]))
    
    return table

def create_goals_summary(matches, console):
    """Creates a summary of goals scored across all matches.
    
    Aggregates goal statistics including total goals scored and top scorers
    from the provided match data.
    
    Args:
        matches (list): List of match dictionaries containing:
            - home_score (int): Home team score
            - away_score (int): Away team score
            - goals (list): List of goal information
        console (Console): Rich console object for display
        
    Returns:
        Text: A Rich Text object containing goal statistics and top scorers
    """
    total_goals = 0
    scorers = {}
    
    for match in matches:
        home_score = match.get("home_score", 0)
        away_score = match.get("away_score", 0)
        total_goals += (home_score + away_score)
        
        for goal in match.get("goals", []):
            player = goal.get("player")
            if player:
                scorers[player] = scorers.get(player, 0) + 1
    
    # Sort top scorers
    top_scorers = sorted(scorers.items(), key=lambda x: x[1], reverse=True)[:5]
    
    summary = Text()
    summary.append(f"Total Goals: ", style="bold")
    summary.append(f"{total_goals}\n\n", style="green")
    
    if top_scorers:
        summary.append("Top Scorers:\n", style="bold")
        for player, goals in top_scorers:
            summary.append(f"• {player}: ", style="cyan")
            summary.append(f"{goals} goal{'s' if goals > 1 else ''}\n", style="green")
    
    return summary
