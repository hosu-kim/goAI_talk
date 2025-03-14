import datetime
import re
from collections import Counter
from difflib import get_close_matches

def get_initial_bot_message():
    """Returns the initial greeting message from the bot"""
    return (
        "Hello! I'm your Football Match Assistant. "
        "Ask me about recent football matches, scores, and results!"
    )

def process_question(question, matches):
    """Process a user question about football matches"""
    if not matches:
        return "I don't have any match data available at the moment. Try refreshing the data with the 'refresh' command."
    
    # Basic question classification
    question = question.lower()
    
    # Handle greetings
    greetings = ['hi', 'hello', 'hey', 'greetings']
    if question in greetings or any(q == question for q in greetings):
        return get_initial_bot_message()
    
    # Extract key information from question
    team_names = extract_team_names(question, matches)
    time_period = extract_time_period(question)
    league_info = extract_league_info(question, matches)
    
    # Handle different question types
    if re.search(r'who won|winner|win|score|result|how did .* do', question):
        return get_match_results(matches, team_names, time_period, league_info)
    
    if re.search(r'fixtures|schedule|upcoming|when|play next|playing', question):
        return "I can only provide information about completed matches at this time."
    
    if team_names:
        return get_match_results(matches, team_names, time_period, league_info)
    
    if league_info:
        return get_league_results(matches, league_info, time_period)
        
    # Default response if no specific question type is identified
    return summarize_recent_matches(matches)

def extract_team_names(question, matches):
    """Extract team names from the question"""
    # Create a list of all team names in the dataset
    all_teams = []
    for match in matches:
        all_teams.append(match.get('homeTeam', {}).get('name', '').lower())
        all_teams.append(match.get('awayTeam', {}).get('name', '').lower())
    
    # Remove duplicates
    all_teams = list(set([team for team in all_teams if team]))
    
    # Look for team names in the question
    found_teams = []
    words = re.findall(r'\b\w+\b', question.lower())
    
    # Check for multi-word team names first
    for i in range(len(words) - 1, 0, -1):
        for j in range(len(words) - i + 1):
            potential_team = " ".join(words[j:j+i])
            matches = get_close_matches(potential_team, all_teams, n=1, cutoff=0.8)
            if matches:
                found_teams.append(matches[0])
    
    # Check for single team name mentions
    for word in words:
        matches = get_close_matches(word, all_teams, n=1, cutoff=0.8)
        if matches and matches[0] not in found_teams:
            found_teams.append(matches[0])
    
    return found_teams

def extract_time_period(question):
    """Extract time period from the question"""
    question = question.lower()
    
    if re.search(r'yesterday|last night', question):
        return 'yesterday'
    elif re.search(r'today|tonight', question):
        return 'today'
    elif re.search(r'this week|past week|recent', question):
        return 'week'
    elif re.search(r'last weekend|weekend', question):
        return 'weekend'
    
    # Default to all available data
    return None

def extract_league_info(question, matches):
    """Extract league information from the question"""
    # Create a list of leagues in the dataset
    all_leagues = []
    for match in matches:
        league = match.get('league', {}).get('name', '').lower()
        if league:
            all_leagues.append(league)
    
    # Common league names and aliases
    league_aliases = {
        'premier league': ['premier league', 'epl', 'english premier league', 'pl'],
        'la liga': ['la liga', 'spanish league', 'primera division'],
        'bundesliga': ['bundesliga', 'german league'],
        'serie a': ['serie a', 'italian league'],
        'ligue 1': ['ligue 1', 'french league']
    }
    
    # Check for league mentions
    question = question.lower()
    
    # Check for direct league names
    for league in all_leagues:
        if league in question:
            return league
    
    # Check for league aliases
    for league, aliases in league_aliases.items():
        if any(alias in question for alias in aliases):
            # Find the correct league name in our dataset
            for actual_league in all_leagues:
                if league in actual_league.lower():
                    return actual_league
            return league
    
    return None

def get_match_results(matches, team_names, time_period, league_info):
    """Get match results for specific teams"""
    if not team_names:
        return "I couldn't identify any specific team in your question."
    
    filtered_matches = []
    
    # Filter by team
    for match in matches:
        home_team = match.get('homeTeam', {}).get('name', '').lower()
        away_team = match.get('awayTeam', {}).get('name', '').lower()
        
        if any(team in [home_team, away_team] for team in team_names):
            filtered_matches.append(match)
    
    # Further filter by time period if specified
    if time_period:
        filtered_matches = filter_by_time(filtered_matches, time_period)
    
    # Further filter by league if specified
    if league_info:
        filtered_matches = [m for m in filtered_matches if 
                           league_info.lower() in m.get('league', {}).get('name', '').lower()]
    
    if not filtered_matches:
        return f"I couldn't find any matches for {', '.join(team_names)} in the specified time period."
    
    # Format results
    response = []
    for match in sorted(filtered_matches, key=lambda m: m.get('fixture', {}).get('date', '')):
        home_team = match.get('homeTeam', {}).get('name', '')
        away_team = match.get('awayTeam', {}).get('name', '')
        home_score = match.get('goals', {}).get('home', 0)
        away_score = match.get('goals', {}).get('away', 0)
        date = match.get('fixture', {}).get('date', '')
        
        if date:
            try:
                date_obj = datetime.datetime.fromisoformat(date.replace('Z', '+00:00'))
                date_str = date_obj.strftime('%Y-%m-%d')
            except:
                date_str = date
        else:
            date_str = "Unknown date"
        
        league_name = match.get('league', {}).get('name', 'Unknown league')
        response.append(f"[{date_str}] {league_name}: {home_team} {home_score}-{away_score} {away_team}")
    
    return "\n".join(response)

def get_league_results(matches, league_info, time_period):
    """Get match results for a specific league"""
    filtered_matches = [m for m in matches if 
                       league_info.lower() in m.get('league', {}).get('name', '').lower()]
    
    if time_period:
        filtered_matches = filter_by_time(filtered_matches, time_period)
    
    if not filtered_matches:
        return f"I couldn't find any matches in {league_info} for the specified time period."
    
    # Format results
    response = [f"Match results for {league_info}:"]
    for match in sorted(filtered_matches, key=lambda m: m.get('fixture', {}).get('date', '')):
        home_team = match.get('homeTeam', {}).get('name', '')
        away_team = match.get('awayTeam', {}).get('name', '')
        home_score = match.get('goals', {}).get('home', 0)
        away_score = match.get('goals', {}).get('away', 0)
        date = match.get('fixture', {}).get('date', '')
        
        if date:
            try:
                date_obj = datetime.datetime.fromisoformat(date.replace('Z', '+00:00'))
                date_str = date_obj.strftime('%Y-%m-%d')
            except:
                date_str = date
        else:
            date_str = "Unknown date"
        
        response.append(f"[{date_str}] {home_team} {home_score}-{away_score} {away_team}")
    
    return "\n".join(response)

def filter_by_time(matches, time_period):
    """Filter matches by time period"""
    today = datetime.datetime.utcnow().date()
    yesterday = today - datetime.timedelta(days=1)
    week_ago = today - datetime.timedelta(days=7)
    
    filtered = []
    for match in matches:
        date = match.get('fixture', {}).get('date', '')
        if not date:
            continue
        
        try:
            date_obj = datetime.datetime.fromisoformat(date.replace('Z', '+00:00')).date()
            
            if time_period == 'today' and date_obj == today:
                filtered.append(match)
            elif time_period == 'yesterday' and date_obj == yesterday:
                filtered.append(match)
            elif time_period == 'week' and week_ago <= date_obj <= today:
                filtered.append(match)
            elif time_period == 'weekend' and week_ago <= date_obj <= today and date_obj.weekday() >= 5:
                filtered.append(match)
        except:
            continue
    
    return filtered

def summarize_recent_matches(matches):
    """Summarize recent matches when no specific query is identified"""
    if not matches:
        return "I don't have any recent match data to share."
    
    # Sort matches by date (newest first)
    sorted_matches = sorted(matches, 
                           key=lambda m: m.get('fixture', {}).get('date', ''),
                           reverse=True)
    
    # Get matches from the last 2 days
    today = datetime.datetime.utcnow().date()
    two_days_ago = today - datetime.timedelta(days=2)
    
    recent_matches = []
    for match in sorted_matches:
        date = match.get('fixture', {}).get('date', '')
        if not date:
            continue
        
        try:
            date_obj = datetime.datetime.fromisoformat(date.replace('Z', '+00:00')).date()
            if date_obj >= two_days_ago:
                recent_matches.append(match)
        except:
            continue
    
    if not recent_matches:
        recent_matches = sorted_matches[:5]  # Just take the 5 most recent
    
    # Count leagues
    leagues = Counter(match.get('league', {}).get('name', 'Unknown') for match in recent_matches)
    top_leagues = leagues.most_common(3)
    
    # Format summary
    summary = ["Here's a summary of recent football matches:"]
    
    for league_name, count in top_leagues:
        summary.append(f"\n{league_name} ({count} matches):")
        league_matches = [m for m in recent_matches if m.get('league', {}).get('name', '') == league_name]
        
        for match in league_matches[:3]:  # Show up to 3 matches per league
            home_team = match.get('homeTeam', {}).get('name', '')
            away_team = match.get('awayTeam', {}).get('name', '')
            home_score = match.get('goals', {}).get('home', 0)
            away_score = match.get('goals', {}).get('away', 0)
            
            summary.append(f"- {home_team} {home_score}-{away_score} {away_team}")
    
    summary.append("\nAsk me about a specific team or league for more details.")
    return "\n".join(summary)
