import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
API_KEY = os.getenv('FOOTBALL_API_KEY')
API_HOST = os.getenv('FOOTBALL_API_HOST', 'v3.football.api-sports.io')
BASE_URL = f"https://{API_HOST}"

# Default headers
headers = {
    'x-rapidapi-key': API_KEY,
    'x-rapidapi-host': API_HOST
}

def fetch_matches_for_date(date_str):
    """Fetch football matches for a specific date"""
    print(f"Fetching matches for date: {date_str}")
    
    endpoint = f"{BASE_URL}/fixtures"
    params = {
        'date': date_str
    }
    
    print(f"API Request: {endpoint}")
    print(f"Params: {params}")
    
    response = None
    try:
        response = requests.get(endpoint, headers=headers, params=params)
        print(f"Response status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"API Response Data:")
            
            matches = []
            results = data.get('response', [])
            completed_count = 0
            
            for fixture in results:
                # Check if the match is finished
                fixture_status = fixture.get('fixture', {}).get('status', {}).get('short')
                
                if fixture_status in ['FT', 'AET', 'PEN']:  # Full time, Extra time, Penalties
                    completed_count += 1
                    
                    # Extract relevant match information
                    match_data = {
                        'fixture': {
                            'id': fixture.get('fixture', {}).get('id'),
                            'date': fixture.get('fixture', {}).get('date'),
                            'venue': fixture.get('fixture', {}).get('venue', {}).get('name'),
                            'status': fixture.get('fixture', {}).get('status', {}).get('long')
                        },
                        'league': {
                            'id': fixture.get('league', {}).get('id'),
                            'name': fixture.get('league', {}).get('name'),
                            'country': fixture.get('league', {}).get('country'),
                            'logo': fixture.get('league', {}).get('logo')
                        },
                        'homeTeam': {
                            'id': fixture.get('teams', {}).get('home', {}).get('id'),
                            'name': fixture.get('teams', {}).get('home', {}).get('name'),
                            'logo': fixture.get('teams', {}).get('home', {}).get('logo'),
                            'winner': fixture.get('teams', {}).get('home', {}).get('winner')
                        },
                        'awayTeam': {
                            'id': fixture.get('teams', {}).get('away', {}).get('id'),
                            'name': fixture.get('teams', {}).get('away', {}).get('name'),
                            'logo': fixture.get('teams', {}).get('away', {}).get('logo'),
                            'winner': fixture.get('teams', {}).get('away', {}).get('winner')
                        },
                        'goals': {
                            'home': fixture.get('goals', {}).get('home'),
                            'away': fixture.get('goals', {}).get('away')
                        },
                        'score': fixture.get('score')
                    }
                    matches.append(match_data)
            
            print(f"Successfully processed {completed_count} completed matches")
            return matches
        else:
            print(f"API request failed with status code: {response.status_code}")
            if response.text:
                print(f"Error message: {response.text}")
            return []
            
    except Exception as e:
        print(f"Error fetching matches: {e}")
        if response:
            print(f"Response: {response.text}")
        return []
