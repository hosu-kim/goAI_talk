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
File: app/models.py
Author: Hosu Kim
Created: 2025-03-21 12:02:29 UTC

Description:
    This module defines Pydantic models for API data validation
'''

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from .domain.domain import GoalEvent, Match

"""
BaseModel:
    1. Data validation
    2. Data parsing
Field:
    1. Metadata provision
    2. Default factory conversion
"""
# ClassName(AnotherClass): Class inheritance
class GoalEventModel(BaseModel):
    """Pydantic model for goal event validation.

    This model validates the data structure of a goal event from the API.
    """
    team: str
    player: str
    minute: int

class MatchModel(BaseModel):
    """Pydantic model for football match validation.

    This model validates the data structure of a football match from the API.
    """
    match_id: int
    date: str
    league: str
    country: str
    home_team: str
    away_team: str
    home_score: int
    away_score: int
    # Using default_factory=list ensures each match instance gets its own independent list,
    # avoiding shared state between different matches
    goal_events: Optional[List[GoalEventModel]] = Field(default_factory=list)

    def to_domain(self) -> Match:
        """Convert this pydantic model to a domain object.

        This method transforms a validation model (Pydantic) into a domain model
        used by the application logic. All fields are transferred and goal events
        are appropriately converted

        Returns:
            Match: A domain Match object constructed from this model's data.
        """
        return Match(
            match_id=self.match_id,
            date=self.date,
            league=self.league,
            country=self.country,
            home_team=self.home_team,
            away_team=self.away_team,
            home_score=self.home_score,
            away_score=self.away_score,
            goal_events=[GoalEvent(
                team=goal.team,
                player=goal.player,
                minute=goal.minute
            ) for goal in self.goal_events]
        )

class RawFixtureModel(BaseModel):
    """Model for fixture information in raw API response."""
    id: int
    date: str

class RawLeagueModel(BaseModel):
    """Model for league information in raw API response."""
    name: str
    country: str

class RawTeamModel(BaseModel):
    """Model for team information in raw API response."""
    name: str

class RawScoreModel(BaseModel):
    """Model for goals information in raw API response."""
    home: Optional[int]
    away: Optional[int]

class RawMatchEventModel(BaseModel):
    """Model for events in raw API response.

    This model validates the event data structure from the API.
    """
    type: str
    team: Dict[str, Any]
    player: Dict[str, Any]
    time: Dict[str, int]

class RawMatchModel(BaseModel):
    """Model for the entire match entry in the raw API response.

    This model validates the complete match data structure from the API.
    """
    fixture: RawFixtureModel
    league: RawLeagueModel
    teams: Dict[str, RawTeamModel]
    goals: RawScoreModel
    events: Optional[List[RawMatchEventModel]] = Field(default_factory=list)

    def to_match_model(self) -> MatchModel:
        """Convert this raw API model to a more structured MatchModel.

        Returns:
            MatchModel: A structured representation of the match data.
        """
        goal_events = []
        for event in self.events:
            if event.type == 'Goal':
                goal_events.append(GoalEventModel(
                    team=event.team.name,
                    player=event.player.name,
                    minute=event.time.elapsed
                ))

        return MatchModel(
            match_id=self.fixture.id,
            date=self.fixture.date,
            league=self.league.name,
            country=self.league.country,
            home_team=self.teams['home'].name,
            away_team=self.teams['away'].name,
            home_score=self.goals.home,
            away_score=self.goals.away,
            goal_events=goal_events
        )

class RawAPIResponse(BaseModel):
    """Model for the entire API response.

    This model validates the complete API response structure.
    """
    response: List[RawMatchModel]
