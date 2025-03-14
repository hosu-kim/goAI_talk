import os
import logging
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv
from llm.response_cache import ResponseCache
from utils.config import load_config, setup_logger

load_dotenv()

class QnAEngine:
    """
    QnA Engine for processing football-related questions using LLM.
    This class handles the integration with OpenAI's API to generate
    natural language response based on provided match data.
    """
    def __init__(self):
        """Initialize and set up API connection"""
        # Load configuration
        self.config = load_config()
        self.logger = setup_logger("football_qa")
        
        # Set up API key
        self.api_key = self.config["openai_api_key"]
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        # Set up model
        self.model = self.config["openai_model"]
        
        # Initialize caching system
        self.cache = ResponseCache()
        
        self.logger.info("QnAEngine initialized by %s at %s",
                        os.getenv("USER", "unknown_user"),
                        self._get_current_time())

    def _get_current_time(self):
        """Format the current time"""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def get_answer(self, question, matches):
        """
        Generate an answer to a user question
        
        Args:
            question (str): User question
            matches (list): List of match data
            
        Returns:
            str: Generated answer
        """
        self.logger.info("Processing question: %s", question)
        
        # Check cache
        cached_response = self.cache.get(question, matches)
        if cached_response:
            self.logger.info("Using cached response")
            return cached_response
        
        try:
            # Prepare match data
            match_context = self._prepare_match_context(matches)
            
            # Initialize API client
            client = OpenAI(api_key=self.api_key)
            
            # Create prompt
            prompt = self._create_prompt(question, match_context)
            
            # Call API
            self.logger.debug("Calling OpenAI API with model: %s", self.model)
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful football match results assistant. You provide accurate information about football matches based on the provided data. Do not make up information not present in the data."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=800
            )
            
            # Extract and return response
            answer = response.choices[0].message.content.strip()
            self.logger.info("Generated answer (length: %d characters)", len(answer))
            
            # Save to cache
            self.cache.set(question, matches, answer)
            
            return answer
            
        except Exception as e:
            self.logger.error("Error generating answer: %s", str(e), exc_info=True)
            return f"Sorry, an error occurred while answering your question: {str(e)}"
    
    def _prepare_match_context(self, matches):
        """
        Convert match data into context information
        
        Args:
            matches (list): List of match data
            
        Returns:
            str: Context information string
        """
        context = "Yesterday's football match results:\n\n"
        
        # Add information for each match
        for i, match in enumerate(matches, 1):
            home = match.get("home_team", "Unknown")
            away = match.get("away_team", "Unknown")
            home_score = match.get("home_score", 0)
            away_score = match.get("away_score", 0)
            league = match.get("league", "Unknown League")
            
            context += f"{i}. [{league}] {home} {home_score} - {away_score} {away}\n"
            
            # Add goal information
            goals = match.get("goals", [])
            if goals:
                context += "   Goal details:\n"
                for goal in goals:
                    player = goal.get("player", "Unknown")
                    team = goal.get("team", "Unknown")
                    minute = goal.get("minute", 0)
                    context += f"   - {minute}min: {player} ({team})\n"
                    
            context += "\n"
        
        return context
        
    def _create_prompt(self, question, match_context):
        """
        Create a prompt for API request
        
        Args:
            question (str): User question
            match_context (str): Match data context
            
        Returns:
            str: Complete prompt
        """
        return f"""Please answer the following question based on the football match data provided:

{match_context}

Question: {question}

Please provide your answer in Korean. Do not speculate on information not included in the data and clearly state if the information is not available."""