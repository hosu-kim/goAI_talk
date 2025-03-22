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
File: app/domain.py
Author: Hosu Kim
Created: 2025-03-21 11:27:48 UTC

Description:
    This module defines Pydantic models for API data validation
'''
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class GoalEvent:
    """Represents a goal scored during a football match.

    Attributes:
        team (str): The team that scored the goal (full team name).
        player (str): The player who scored the goal (full player name).
        minute (int): The minute when the goal was scored (match time).
    """
    team: str
    player: str
    minute: int

@dataclass
class Match:
    """Represents a football match with its details.

    Attributes:
        match_id (int): Unique identifier for the match.
        date (str): The date when the match was played.
        league (str): The league in which the match was played.
        country (str): The country of the league.
        home_tema (str): Name of the home team.
        away_team (str): Name of the away team.
        home_score (Optional[int]): Goals scored by the home team, if available.
        away_score (Optional[int]): Goals scored by the away team, if available.
        goals (List[GoalEvent]): List of goal events in the match.
"""
    match_id: int
    date: str
    league: str
    country: str
    home_team: str
    away_team: str
    home_score: Optional[int]
    away_score: Optional[int]
    goals: List[GoalEvent]