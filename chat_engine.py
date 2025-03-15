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
File: chat_engine.py
Author: hosu-kim
Created: 2025-03-14 14:22:18 UTC

Description:
    This module handles the processing of user questions related to football matches
    and generates appropriate responses using available match data.
"""

import os
import json
from datetime import datetime, timedelta
import re
from typing import List, Dict, Any
from dotenv import load_dotenv
from utils.config import setup_logger

# Load environment variables with explicit path
dotenv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
load_dotenv(dotenv_path)
logger = setup_logger("chat_engine")

# Check API key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    logger.error("OPENAI_API_KEY environment variable not set")
    print("Error: OPENAI_API_KEY not found in environment variables. Please check your .env file.")
    # Try to debug the .env file loading
    env_file = dotenv_path
    if os.path.exists(env_file):
        logger.info(f".env file exists at {env_file}")
        # Check if the file contains the key (without printing the actual key)
        with open(env_file, 'r') as f:
            content = f.read()
            if "OPENAI_API_KEY" in content:
                logger.info("OPENAI_API_KEY found in .env file but not loaded properly")
            else:
                logger.error("OPENAI_API_KEY not found in .env file")
    else:
        logger.error(f".env file not found at {env_file}")
else:
    # Mask the API key for logging (show only first 3 and last 3 chars)
    masked_key = api_key[:3] + "..." + api_key[-3:] if len(api_key) > 6 else "***"
    logger.info(f"OpenAI API key loaded: {masked_key}")

# Try to use new client, fall back to old if needed
try:
    from openai import OpenAI
    # Handle different API key formats
    if api_key and api_key.startswith("sk-proj-"):
        # For project-based API keys, try to extract the organization
        # Try both the project key as is and alternatives
        try:
            # Option 1: Use the key as is
            client = OpenAI(api_key=api_key)
            logger.info("Using modern OpenAI client with project API key")
            use_modern_client = True
        except Exception as e1:
            # Option 2: If it fails, try with only the first part
            try:
                # Extract just the base key part before the first dot or similar separator
                base_key = api_key.split(".")[0] if "." in api_key else api_key
                client = OpenAI(api_key=base_key)
                logger.info("Using modern OpenAI client with modified project API key")
                use_modern_client = True
                # Update the api_key to use for future calls
                api_key = base_key
            except Exception as e2:
                # Option 3: Try to use a standard key format
                try:
                    standard_key = "sk-" + api_key.split("-")[1] if "-" in api_key else api_key
                    client = OpenAI(api_key=standard_key)
                    logger.info("Using modern OpenAI client with standard API key format")
                    use_modern_client = True
                    # Update the api_key to use for future calls
                    api_key = standard_key
                except Exception as e3:
                    logger.error(f"Failed to initialize client with project key: {e1}")
                    logger.error(f"Failed to initialize client with base key: {e2}")
                    logger.error(f"Failed to initialize client with standard key: {e3}")
                    print(f"Error: Unable to use the provided OpenAI API key. The key may be in an unsupported format.")
                    use_modern_client = False
    else:
        # For standard API keys
        client = OpenAI(api_key=api_key)
        logger.info("Using modern OpenAI client with standard API key")
        use_modern_client = True
except ImportError:
    # Fall back to legacy client
    import openai
    openai.api_key = api_key
    use_modern_client = False
    logger.info("Using legacy OpenAI client")
except Exception as e:
    logger.error(f"Error initializing OpenAI client: {str(e)}")
    print(f"Error initializing OpenAI client: {str(e)}")
    use_modern_client = False
    try:
        import openai
        openai.api_key = api_key
        logger.info("Falling back to legacy client due to errors")
    except Exception as e2:
        logger.error(f"Also failed to initialize legacy client: {str(e2)}")

def process_question(question: str, matches: List[Dict[str, Any]]) -> str:
    """
    Process a user question about football matches and return a relevant answer.
    
    Args:
        question: The user's question as a string
        matches: List of match data dictionaries
        
    Returns:
        A string containing the answer to the question
    """
    logger.info(f"Processing question: {question}")
    
    if not matches:
        return "I don't have any match data available. Please try refreshing the data."
    
    # Create a context with relevant match data
    context = prepare_context(question, matches)
    
    # Generate response using OpenAI
    try:
        response = generate_response(question, context)
        logger.info("Successfully generated response")
        return response
    except Exception as e:
        logger.error(f"Error generating response: {str(e)}", exc_info=True)
        return f"Sorry, I encountered an error while processing your question. Error: {str(e)}"

def prepare_context(question: str, matches: List[Dict[str, Any]]) -> str:
    """
    Prepare context for the question by filtering relevant matches.
    
    Args:
        question: The user's question
        matches: List of all available matches
        
    Returns:
        A string with relevant match data formatted as context
    """
    logger.debug("Preparing context for question")
    
    # Extract potential entity mentions (teams, leagues, dates)
    team_mentions = extract_team_mentions(question, matches)
    league_mentions = extract_league_mentions(question, matches)
    date_mentions = extract_date_mentions(question)
    
    # Filter matches based on extracted entities
    filtered_matches = matches
    
    if team_mentions:
        filtered_matches = [m for m in filtered_matches if 
                           any(team.lower() in m["home_team"].lower() or 
                              team.lower() in m["away_team"].lower() 
                              for team in team_mentions)]
    
    if league_mentions:
        filtered_matches = [m for m in filtered_matches if 
                           any(league.lower() in m["league"].lower() 
                              for league in league_mentions)]
    
    if date_mentions:
        filtered_matches = [m for m in filtered_matches if 
                           any(date in m["date"] for date in date_mentions)]
    
    # If no specific filters matched, use all matches but limit number to avoid context window issues
    if len(filtered_matches) == len(matches) and len(filtered_matches) > 10:
        # Sort by recency and keep most recent matches
        filtered_matches = sorted(filtered_matches, key=lambda m: m["date"], reverse=True)[:10]
    
    # Format context
    context_parts = []
    context_parts.append(f"Today's date is {datetime.utcnow().strftime('%Y-%m-%d')}.")
    context_parts.append(f"The following are recent football match results:")
    
    for match in filtered_matches:
        match_str = (f"Date: {match['date']}, "
                    f"League: {match['league']}, "
                    f"Match: {match['home_team']} {match['home_score']} - {match['away_score']} {match['away_team']}")
        
        if match["goals"]:
            goals_str = ", Goals: " + "; ".join(
                f"{g['player']} ({g['team']}, {g['minute']})" 
                for g in match["goals"]
            )
            match_str += goals_str
            
        context_parts.append(match_str)
    
    return "\n".join(context_parts)

def extract_team_mentions(question: str, matches: List[Dict[str, Any]]) -> List[str]:
    """Extract team names from the question."""
    team_names = set()
    for match in matches:
        team_names.add(match["home_team"])
        team_names.add(match["away_team"])
    
    found_teams = []
    for team in team_names:
        if team.lower() in question.lower():
            found_teams.append(team)
    
    return found_teams

def extract_league_mentions(question: str, matches: List[Dict[str, Any]]) -> List[str]:
    """Extract league names from the question."""
    league_names = set(match["league"] for match in matches)
    
    found_leagues = []
    for league in league_names:
        if league.lower() in question.lower():
            found_leagues.append(league)
    
    # Also check for common league abbreviations
    if "epl" in question.lower() or "premier league" in question.lower():
        for league in league_names:
            if "premier league" in league.lower() and "england" in league.lower():
                found_leagues.append(league)
    
    return found_leagues

def extract_date_mentions(question: str) -> List[str]:
    """Extract date references from the question."""
    today = datetime.utcnow().date()
    dates = []
    
    # Check for "yesterday", "today", etc.
    if "yesterday" in question.lower():
        yesterday = (today - timedelta(days=1)).strftime("%Y-%m-%d")
        dates.append(yesterday)
    
    if "today" in question.lower():
        dates.append(today.strftime("%Y-%m-%d"))
    
    if "last week" in question.lower() or "past week" in question.lower():
        for i in range(1, 8):
            past_date = (today - timedelta(days=i)).strftime("%Y-%m-%d")
            dates.append(past_date)
    
    # Check for explicit dates (YYYY-MM-DD format)
    date_pattern = r'\d{4}-\d{2}-\d{2}'
    explicit_dates = re.findall(date_pattern, question)
    dates.extend(explicit_dates)
    
    return dates

def generate_response(question: str, context: str) -> str:
    """
    Generate a response to the question using the OpenAI API.
    
    Args:
        question: User's question
        context: Context with relevant match data
        
    Returns:
        Generated response as a string
    """
    # First check if the API key is set
    if not api_key:
        return "OpenAI API key is missing. Please make sure it's correctly set in the .env file."
    
    logger.debug("Generating response using OpenAI")
    
    system_prompt = """
    You are a helpful football match results assistant. You have access to information about 
    recent football matches and can answer questions about scores, teams, goals, and other match details.
    Always be concise and to the point. If you don't have information to answer a question, 
    be honest about it. Don't make up facts or scores that aren't in your context.
    """
    
    try:
        # Use a simpler fallback approach - create a dummy response if API fails
        try:
            if use_modern_client and 'client' in globals():
                logger.debug("Calling OpenAI API with modern client...")
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": f"Here's some information about recent football matches:\n\n{context}"},
                        {"role": "user", "content": question}
                    ],
                    temperature=0.7,
                    max_tokens=500
                )
                answer = response.choices[0].message.content
            else:
                # Legacy client
                logger.debug("Calling OpenAI API with legacy client...")
                import openai
                openai.api_key = api_key
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": f"Here's some information about recent football matches:\n\n{context}"},
                        {"role": "user", "content": question}
                    ],
                    temperature=0.7,
                    max_tokens=500
                )
                answer = response.choices[0].message.content
                
            logger.info("Successfully received response from OpenAI")
            return answer
        
        except Exception as api_error:
            logger.error(f"OpenAI API error: {str(api_error)}")
            
            # If API fails, attempt a simple fallback response based on the context
            logger.info("Using fallback response generation")
            
            # Very basic response generation based on keywords
            q_lower = question.lower()
            if "who won" in q_lower or "winner" in q_lower:
                for match in context.split('\n'):
                    if "Match:" in match:
                        teams_scores = match.split("Match:")[1].strip()
                        home_team, rest = teams_scores.split(" ", 1)
                        away_score = rest.split(" ")[-1]
                        home_score = rest.split(" ")[0]
                        if home_score > away_score:
                            return f"Based on the match data, {home_team} won."
                        elif away_score > home_score:
                            return f"Based on the match data, {away_team} won."
                        else:
                            return "The match ended in a draw."
            
            if "score" in q_lower:
                for match in context.split('\n'):
                    if "Match:" in match:
                        return f"Here is the score information: {match.split('Match:')[1].strip()}"
            
            # Default fallback response
            return (
                "I apologize, but I'm having trouble accessing the AI service. "
                "Here's the data I have available:\n\n" + context
            )
            
    except Exception as e:
        logger.error(f"Error generating response: {str(e)}", exc_info=True)
        
        error_msg = str(e).lower()
        if "api key" in error_msg or "apikey" in error_msg or "authentication" in error_msg:
            return (
                "OpenAI API key issue detected. Please check that:\n"
                "1. Your .env file contains the OPENAI_API_KEY variable\n"
                "2. The API key is valid and not expired\n"
                "3. You have billing set up for your OpenAI account\n\n"
                f"Error details: {str(e)}"
            )
        elif "rate limit" in error_msg or "quota" in error_msg:
            return "I'm sorry, the OpenAI API rate limit has been reached. Please try again later."
        else:
            return f"I'm sorry, there was an error processing your request: {str(e)}"

def find_team_by_partial_name(partial_name: str, matches: List[Dict[str, Any]]) -> List[str]:
    """Find teams that match a partial name."""
    team_names = set()
    for match in matches:
        team_names.add(match["home_team"])
        team_names.add(match["away_team"])
    
    matching_teams = []
    for team in team_names:
        if partial_name.lower() in team.lower():
            matching_teams.append(team)
    
    return matching_teams
