"""SQLAlchemy models for the football match database.

This module defines the ORM models for storing football match data,
including Match and Goal models.

Author: hosu-kim
Created: 2025-03-14
Version: 1.2.0
"""

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import List, Dict, Any

Base = declarative_base()

class Match(Base):
    """Football match model.
    
    This model represents a football match with teams, scores, and other details.
    """
    
    __tablename__ = 'matches'
    
    id = Column(Integer, primary_key=True)
    date = Column(String, index=True)
    home_team = Column(String, index=True)
    away_team = Column(String, index=True)
    home_score = Column(Integer)
    away_score = Column(Integer)
    league = Column(String, index=True)
    fixture_id = Column(Integer, unique=True, index=True)
    venue = Column(String, nullable=True)
    match_time = Column(String, nullable=True)
    last_updated = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    goals = relationship("Goal", back_populates="match", cascade="all, delete-orphan")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert match data to dictionary.
        
        Returns:
            The match data as a dictionary.
        """
        return {
            "id": self.id,
            "date": self.date,
            "home_team": self.home_team,
            "away_team": self.away_team,
            "home_score": self.home_score,
            "away_score": self.away_score,
            "league": self.league,
            "fixture_id": self.fixture_id,
            "venue": self.venue,
            "match_time": self.match_time,
            "goals": [goal.to_dict() for goal in self.goals],
        }

class Goal(Base):
    """Goal information model.
    
    This model represents a goal scored in a match, including player,
    team, and timing information.
    """
    
    __tablename__ = 'goals'
    
    id = Column(Integer, primary_key=True)
    match_id = Column(Integer, ForeignKey('matches.id'))
    team = Column(String)
    player = Column(String, index=True)
    minute = Column(Integer)
    goal_type = Column(String)
    
    # Relationships
    match = relationship("Match", back_populates="goals")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert goal data to dictionary.
        
        Returns:
            The goal data as a dictionary.
        """
        return {
            "team": self.team,
            "player": self.player,
            "minute": self.minute,
            "type": self.goal_type
        }

def init_db(db_path: str):
    """Initialize the database and create tables if they don't exist.
    
    Args:
        db_path: Path to the SQLite database file.
        
    Returns:
        The SQLAlchemy engine instance.
    """
    engine = create_engine(f'sqlite:///{db_path}')
    Base.metadata.create_all(engine)
    return engine
