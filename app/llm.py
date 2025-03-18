"""Interperter and Encoding setup"""
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
File: app/llm.py
Author: Hosu Kim
Created: 2025-03-14 11:15:03 UTC

Description:
    The QnAEngine class fetches yesterday's football match results and generates responses using OpenAI's GPT-3.5-turbo. 
    It handles conversation history, token limits, and formats answers accordingly.
'''

import openai
import config
from app.database_manager.database import Database
import os

class QnAEngine:
    """A Question-Answering engine for yesterday football match results using OpenAI's API.

    This class handles the interaction with OpenAI's API to generate responses
    about yesterday's football match results. It maintains conversation history and handles
    token limitations while formatting response appropriately.

    Attributes:
        client (openai.Client): OpenAI API client instance.
        db (Database): Database instance for match data access.
        max_token_limit (int): Maximum tokens allowed in API context (16,385 for GPT-3.5).
        match_limit (int): Maximum number of matches to include in context.
        conversation_history (list): List of prior conversation messages
    """
    def __init__(self, match_limit=config.MATCH_LIMIT):
        """Initialize the QnAEngine with configuration parameters.

        Args:
            match_limit (int, optional): Maximum number of matches to inclue in context.
                                       Defaults to value in config.MATCH_LIMIT.
        """
        db_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'database_manager',
            'football_data.db'
        )
        self.client = openai.Client(api_key=config.OPENAI_API_KEY)
        self.db = Database(db_path=db_path)
        self.max_token_limit = 16385 # GTP-3.5-turbo context window size
        self.match_limit = match_limit
        self.conversation_history = []

    def get_answer(self, question):
        """Generate an answer to the user's question about football matches.

        Args:
            question (str): User's question about football matches

        Returns:
            str: Generated answer or error message
        """
        matches = self.db.get_yesterdays_matches_from_db()
        
        if not matches:
            return "Sorry, there is no match data available at the moment."

        limited_matches = self._limit_matches_by_size(matches)
        
        # Update conversation history
        self.conversation_history.append({"role": "user", "content": question})
        
        # Keep recent converations based on config limit
        if len(self.conversation_history) > config.MAX_CONVERSATION_HISTORY * 2:
            self.conversation_history = self.conversation_history[
                -(config.MAX_CONVERSATION_HISTORY * 2):
            ]

        # Prepare messages for API
        messages = [
            {"role": "system", "content": self._create_prompt(limited_matches)},
            *self.conversation_history
        ]

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages
            )
            answer = response.choices[0].message.content
            
            # Store assistant's response
            self.conversation_history.append({
                "role": "assistant",
                "content": answer
            })

            return answer
        except Exception as e:
            print(f"\nAPI Error Details:")
            print(f"Error Type: {type(e).__name__}")
            print(f"Error Message: {str(e)}")
            print(f"Error Details: {e.__dict__}")
            return []
    def _retry_with_less_data(self, question, matches):
        """Retry answer generation with reuced match data.

        Args:
            question (str): Original question
            matches (list): Match data list

        Returns:
            str: Generated answer or error message
        """
        try:
            reduced_matches = self._limit_matches_by_size(
                matches,
                self.match_limit - 10
            )
            messages = [
                {"role": "system", "content": self._create_prompt(question, reduced_matches)},
                {"role": "user", "content": question}
            ]

            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Failed to generate answer: {str(e)}"

    def _limit_matches_by_size(self, matches):
        """Limit the number of matches to process.

        Args:
            matches (list): List of match dictionaries

        Returns:
            list: Limited list of matches based on self.match_limit
        """
        return matches[:self.match_limit]

    def _create_prompt(self, matches):
        """Create system prompt for the LLM.

        Args:
            matches (list): List of match dictionaries containing match information

        Returns:
            str: Formatted system prompt with match data
        """
        match_count = len(matches)
        
        prompt = f"""You are a friendly and knowledgeable yesterday's football match results assistant.
                     Your role is to provide clear, properly formatted, and detailed information about yesterday's football matches.
                     You should answer in the same language as the user's question.

                     FORMATTING REQUIREMENTS:
                         1. Format your responses with proper alignment and structure
                         2. Use consistent indentation and spacing
                         3. For tabular data (like match results), maintain proper alignment
                         4. When listing matches, use a consistent format for all entries
                         5. Use appropriate headers and separators for different sections
                         6. Avoid extraneous whitespace characters that could disrupt terminal display
                         7. Do not add extra spaces at the beginning of lines
                         8. Format match results in a clean, structured way, e.g.:
                             • Liga MX (Mexico):
                             • Atlas W 2-1 Monterrey W
                             • Necaxa W 1-0 León W
                         9. For multiple leagues, use clear section headers
                         10. For statistics, use consistent formatting throughout

                     Available Matches: {match_count}

                     Match Data:
        """
        # Add match information
        for match in matches:
            prompt += f"""
            {match['league']} ({match['country']}):
            {match['home_team']} {match['home_score']} - {match['away_score']} {match['away_team']}
            """
        return prompt
