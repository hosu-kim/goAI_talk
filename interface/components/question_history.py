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
File: interface/components/question_history.py
Author: hosu-kim
Created: 2024-03-14

Description:
    This module manages the user question history functionality
    including storage, retrieval and display of past questions
    using Rich library components.
"""
import json
import os
from datetime import datetime
from rich.table import Table

class QuestionHistory:
    """Manages user question history with persistence and display functionality.
    
    This class handles storing, retrieving, and displaying user questions and their
    answers, with support for local file storage and rich text formatting.
    """
    
    def __init__(self, history_file="question_history.json"):
        """Initializes the question history manager.
        
        Args:
            history_file (str): Path to the JSON file for storing question history
        """
        self.history_file = history_file
        self.history = self._load_history()
        
    def _load_history(self):
        """Loads question history from the JSON file.
        
        Returns:
            list: List of question history entries. Returns empty list if file
                 doesn't exist or is corrupted.
        """
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def _save_history(self):
        """Save question history to file"""
        with open(self.history_file, 'w') as f:
            json.dump(self.history, f, indent=2)
    
    def add_question(self, question, answer=None):
        """Adds a new question and optional answer to the history.
        
        Args:
            question (str): The user's question
            answer (str, optional): The system's response
        """
        self.history.append({
            "timestamp": datetime.utcnow().isoformat(),
            "question": question,
            "answer": answer
        })
        
        # Keep only the last 100 questions
        if len(self.history) > 100:
            self.history = self.history[-100:]
            
        self._save_history()
    
    def get_recent_questions(self, count=5):
        """
        Get recent questions
        
        Args:
            count (int): Number of questions to retrieve
        
        Returns:
            list: List of recent questions
        """
        return self.history[-count:]
    
    def create_history_table(self, count=5):
        """Creates a formatted table of recent questions.
        
        Args:
            count (int): Number of recent questions to include
            
        Returns:
            Table: Rich Table object containing recent questions
        """
        table = Table(title="Recent Questions")
        table.add_column("Time", style="dim")
        table.add_column("Question", style="cyan")
        
        recent = self.get_recent_questions(count)
        
        if not recent:
            table.add_row("N/A", "No previous questions")
            return table
        
        for item in reversed(recent):
            # Convert ISO format time to readable format
            timestamp = item.get("timestamp", "")
            try:
                dt = datetime.fromisoformat(timestamp)
                time_str = dt.strftime("%H:%M:%S")
            except:
                time_str = "Unknown"
                
            question = item.get("question", "")
            # Truncate question if too long
            if len(question) > 50:
                question = question[:47] + "..."
                
            table.add_row(time_str, question)
            
        return table
    
    def search_questions(self, keyword):
        """Searches question history for a specific keyword.
        
        Args:
            keyword (str): Search term to look for in questions
            
        Returns:
            list: List of matching question entries
        """
        keyword = keyword.lower()
        results = []
        
        for item in self.history:
            question = item.get("question", "").lower()
            if keyword in question:
                results.append(item)
                
        return results
    
    def clear_history(self):
        """Clear question history"""
        self.history = []
        self._save_history()
