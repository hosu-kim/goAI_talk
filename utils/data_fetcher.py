import os
import json
from datetime import datetime, timedelta, timezone

def fetch_matches(date=None, use_test_data=True):
    """Fetch match data from test data or live API.
    
    Args:
        date (str): Date in YYYY-MM-DD format
        use_test_data (bool): Whether to use test data instead of live API
        
    Returns:
        list: List of match data dictionaries
    """
    if date is None:
        date = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    
    if use_test_data:
        test_data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'test_data', 'sample_matches.json')
        try:
            with open(test_data_path, 'r') as f:
                test_matches = json.load(f)
            
            all_matches = []
            date_obj = datetime.strptime(date, '%Y-%m-%d')
            
            for i in range(-1, 2):
                check_date = (date_obj + timedelta(days=i)).strftime('%Y-%m-%d')
                if check_date in test_matches:
                    all_matches.extend(test_matches[check_date])
            
            if not all_matches:
                print("\nNo matches found in test data for the specified dates.")
                print("Available dates in test data:", ', '.join(test_matches.keys()))
            
            return all_matches
            
        except FileNotFoundError:
            print("Test data file not found. Using live API...")
            use_test_data = False
    
    return []  # Empty list if no matches found or not using test data

import os
import json
from datetime import datetime
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def fetch_matches(date_str, use_test_data=False):
    """
    Fetch football matches for a specified date
    
    Args:
        date_str (str): Date string in YYYY-MM-DD format
        use_test_data (bool): Whether to use test data instead of API
        
    Returns:
        list: List of match dictionaries
    """
    if use_test_data:
        return _get_test_matches(date_str)
    
    # Import locally to avoid circular imports
    from football_api import fetch_matches_for_date
    
    matches = fetch_matches_for_date(date_str)
    return matches

def _get_test_matches(date_str):
    """Get test match data for development/testing"""
    # Sample match data for testing
    test_matches = [
        {
            "fixture": {
                "id": 1000001,
                "date": f"{date_str}T19:45:00+00:00",
                "venue": "Old Trafford",
                "status": "Match Finished"
            },
            "league": {
                "id": 39,
                "name": "Premier League",
                "country": "England",
                "logo": "https://media.api-sports.io/football/leagues/39.png"
            },
            "teams": {
                "home": {
                    "id": 33,
                    "name": "Manchester United",
                    "logo": "https://media.api-sports.io/football/teams/33.png",
                    "winner": True
                },
                "away": {
                    "id": 40,
                    "name": "Liverpool",
                    "logo": "https://media.api-sports.io/football/teams/40.png",
                    "winner": False
                }
            },
            "goals": {
                "home": 3,
                "away": 1
            },
            "score": {
                "halftime": {
                    "home": 1,
                    "away": 0
                },
                "fulltime": {
                    "home": 3,
                    "away": 1
                }
            }
        },
        {
            "fixture": {
                "id": 1000002,
                "date": f"{date_str}T17:30:00+00:00",
                "venue": "Etihad Stadium",
                "status": "Match Finished"
            },
            "league": {
                "id": 39,
                "name": "Premier League",
                "country": "England",
                "logo": "https://media.api-sports.io/football/leagues/39.png"
            },
            "teams": {
                "home": {
                    "id": 50,
                    "name": "Manchester City",
                    "logo": "https://media.api-sports.io/football/teams/50.png",
                    "winner": True
                },
                "away": {
                    "id": 47,
                    "name": "Tottenham",
                    "logo": "https://media.api-sports.io/football/teams/47.png",
                    "winner": False
                }
            },
            "goals": {
                "home": 2,
                "away": 0
            },
            "score": {
                "halftime": {
                    "home": 1,
                    "away": 0
                },
                "fulltime": {
                    "home": 2,
                    "away": 0
                }
            }
        },
        {
            "fixture": {
                "id": 1000003,
                "date": f"{date_str}T20:00:00+00:00",
                "venue": "Camp Nou",
                "status": "Match Finished"
            },
            "league": {
                "id": 140,
                "name": "La Liga",
                "country": "Spain",
                "logo": "https://media.api-sports.io/football/leagues/140.png"
            },
            "teams": {
                "home": {
                    "id": 529,
                    "name": "Barcelona",
                    "logo": "https://media.api-sports.io/football/teams/529.png",
                    "winner": None
                },
                "away": {
                    "id": 541,
                    "name": "Real Madrid",
                    "logo": "https://media.api-sports.io/football/teams/541.png",
                    "winner": None
                }
            },
            "goals": {
                "home": 2,
                "away": 2
            },
            "score": {
                "halftime": {
                    "home": 1,
                    "away": 1
                },
                "fulltime": {
                    "home": 2,
                    "away": 2
                }
            }
        }
    ]
    
    return test_matches

def save_matches_to_file(matches, file_path):
    """Save matches data to a JSON file"""
    try:
        # Ensure directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, 'w') as f:
            json.dump(matches, f, indent=2)
        
        return True
    except Exception as e:
        print(f"Error saving matches to file: {e}")
        return False

def load_matches_from_file(file_path):
    """Load matches data from a JSON file"""
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                return json.load(f)
        return []
    except Exception as e:
        print(f"Error loading matches from file: {e}")
        return []
