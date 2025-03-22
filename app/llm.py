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

from typing import List, Dict, Optional
from config import Settings
import logging
from app.database_manager.database import Database
from openai import OpenAI
from openai.types.chat import ChatCompletion
from app.domain.domain import Match
from app.exceptions import DataProcessingError, APIConnectionError


# Get a logger for this module
logger = logging.getLogger(__name__)

class QnAEngine:
    """A Question-Answering engine for yesterday football match results using OpenAI's API."""
    config: Settings
    client: OpenAI
    db: Database
    max_token_limit: int
    match_limit: int
    conversation_history: List[Dict[str, str]]

    def __init__(self, config: Settings, db: Database) -> None:
        """Initialize the QnAEngine with configuration and an injected Database instance."""
        self.config = config
        self.client = OpenAI(api_key=self.config.openai_api_key.get_secret_value())
        self.db = db
        self.max_token_limit = 16385 # GTP-3.5-turbo context window size
        self.match_limit = self.config.match_limit
        self.conversation_history = []
        logger.info(f"QnAEngine initialized with match_limit={self.match_limit}")

    def get_answer(self, question: str) -> str:
        """
        Generate an answer to the user's question regarding football matches.

        Args:
            question (str): The user's question.
        Returns:
            str: The generated answer.
        Raises:
            DataProcessingError: If there is no match data or an error retrieving data.
            APIConnectionError: If there is an error connecting to the OpenAI API.
        """
        logger.info(f"Processing question: '{question}'")
        try:
            matches: List[Match] = self.db.retrieve_yesterdays_matches_from_db()
            if not matches:
                error_msg = "No match data available"
                logger.error(error_msg)
                return DataProcessingError(error_msg)

            limited_matches: List[Match] = self._limit_matches_by_size(matches)
            logger.debug(f"Using {len(limited_matches)} matches for answering")

            # Update conversation history
            self.conversation_history.append({"role": "user", "content": question})
            logger.debug(f"conversation history size: {len(self.conversation_history)}")

            # Keep recent converations based on config limit
            if len(self.conversation_history) > self.config.max_conversation_history * 2:
                self.conversation_history = self.conversation_history[
                    -(self.config.max_conversation_history * 2):
                ]
                logger.debug(f"Trimmed conversation history to {len(self.conversation_history)} entries")

            # Prepare messages for API request using the system prompt and coversation history
            messages: List[Dict[str, str]] = [
                {"role": "system", "content": self._create_prompt(limited_matches)},
                *self.conversation_history
            ]

            try:
                logger.debug("Sending request to OpenAI API")
                response: ChatCompletion = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=messages
                )
                answer: str = response.choices[0].message.content
                logger.debug("Received response from OpenAI API")

                # Log a truncated version of the answer to avoid excessive logging.
                truncated_answer = answer[:100] + "..." if len(answer) > 100 else answer
                logger.info(f"Generated answer: '{truncated_answer}'")

                self.conversation_history.append({"role": "assistant", "content": answer})
                return answer

            except Exception as e:
                error_msg = f"Error connecting to OpenAI API: {str(e)}"
                logger.error(error_msg, exc_info=True)
                raise APIConnectionError(error_msg)

        except DataProcessingError as e:
            # Log the error but let it propagate to the caller for handling
            logger.error(f"Data processing error: {str(e)}", exc_info=True)
            raise
        except APIConnectionError as e:
            # Log the error but let it propagate to the caller for handling
            logger.error(f"API connection error: {str(e)}", exc_info=True)
            raise

    def _retry_with_less_data(self, question: str, matches: List[Match]) -> str:
        """Retry answer generation with reduced match data when initial attempt fails.

        Args:
            question (str): The user's question
            matches (List[Match]): The original list of matches.

        Returns:
            str: The generated answer with reduced data.

        Raises:
            APIConnectionError: If there is an error connecting to the OpenAI API.
        """
        try:
            logger.info("Retrying with reduced match data")
            reduced_limit = max(1, self.match_limit - 10)
            logger.debug(f"Reduced match limit to {reduced_limit}")
            reduced_matches: List[Match] = self._limit_matches_by_size(matches, reduced_limit)

            messages: List[Dict[str, str]] = [
                {"role": "system", "content": self._create_prompt(reduced_matches)},
                {"role": "user", "content": question}
            ]

            logger.debug("Sending retry request to OpenAI API")
            response: ChatCompletion = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages
            )
            answer = response.choices[0].message.content
            logger.info("Successfully generated answer with reduced data")
            return answer

        except Exception as e:
            error_msg = f"Failed to retry with reduced data: {str(e)}"
            logger.error(error_msg, exc_info=True)
            raise APIConnectionError(error_msg)

    def _limit_matches_by_size(self, matches: List[Match], limit: Optional[int] = None) -> List[Match]:
        """
        Limit the number of matches in the list to avoid token limit issues.

        Args:
            matches (List[Match]): The original list of matches.
            limit (Optional[int]): Maximum number of matches to include.
                                  If None, uses self.match_limit.

        Returns:
            List[Match]: A limited subset of the original matches list.
        """
        limit_to_use: int = limit if limit is not None else self.match_limit
        logger.debug(f"Limiting matches to {limit_to_use} (from {len(matches)} total)")
        return matches[:limit_to_use]

    def _create_prompt(self, matches: List[Match]) -> str:
        """
        Create system prompt for the language model based on match data.

        Args:
            matches (List[Match]): The matches to include in the prompt.

        Returns:
            str: A formatted system prompt containing match data.
        """
        match_count: int = len(matches)
        logger.debug(f"Creating prompt with {match_count} matches")

        prompt: str = f"""You are a friendly and knowledgeable yesterday's football match results assistant.
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
        # Append match information using domain object attributes
        for match in matches:
            country = match.country if match.country else "Unknown country"
            prompt += f"\n{match.league} ({country}):"
            prompt += f"\n{match.home_team} {match.home_score} vs {match.away_score} {match.away_team}\n"
            

        # Log a truncated version of the prompt to avoid excessive logging
        truncated_prompt = prompt[:200] + "..." if len(prompt) > 200 else prompt
        logger.debug(f"Created promt: {truncated_prompt}")
        return prompt
