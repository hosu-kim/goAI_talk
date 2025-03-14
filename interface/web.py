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
File: interface/web.py
Author: hosu-kim
Created: 2025-03-14 12:30:45 UTC

Description:
    This module provides the web interface for the Football Q&A system.
    It implements a Flask application with API endpoints and chat functionality.
"""
import sys
import os

# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from utils.config import setup_logger
from datetime import datetime
from utils.data_utils import get_yesterday_date

# Load environment variables
load_dotenv()

app = Flask(__name__, 
            static_folder="../static", 
            template_folder="../templates")

# Setup logger
logger = setup_logger("web_interface")

# Global variables for app context
db_manager = None
qna_engine = None

@app.route('/')
def home():
    """
    Root endpoint that renders the index template
    """
    return render_template('index.html')

@app.route('/api/matches', methods=['GET'])
def get_matches():
    """
    API endpoint to get match data
    """
    try:
        date = request.args.get('date', get_yesterday_date())
        matches = db_manager.get_matches(date)
        return jsonify({
            'status': 'success',
            'matches': matches
        })
    except Exception as e:
        logger.error(f"Error retrieving matches: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/leagues', methods=['GET'])
def get_leagues():
    """
    API endpoint to get league data
    """
    try:
        date = request.args.get('date', get_yesterday_date())
        leagues = db_manager.get_leagues(date)
        return jsonify({
            'status': 'success',
            'leagues': leagues
        })
    except Exception as e:
        logger.error(f"Error retrieving leagues: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/chat', methods=['POST'])
def chat():
    """
    Chat endpoint that handles message processing
    Returns JSON response with chat result
    """
    try:
        # Get JSON data from request
        data = request.get_json()
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({
                'status': 'error',
                'message': 'No message provided'
            }), 400
            
        # Get yesterday's matches
        yesterday = get_yesterday_date()
        matches = db_manager.get_matches(yesterday)
        
        if not matches:
            return jsonify({
                'status': 'warning',
                'response': 'No match data available for yesterday.'
            })
        
        # Get answer from QnA engine
        logger.info(f"Processing question: {user_message}")
        answer = qna_engine.get_answer(user_message, matches)
        logger.info("Answer generated successfully")
        
        return jsonify({
            'status': 'success',
            'response': answer
        })

    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}", exc_info=True)
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

def run_web_app(database_manager, qa_engine, host='0.0.0.0', port=8000, debug=False):
    """
    Run the Flask web application
    
    Args:
        database_manager: Instance of DBManager
        qa_engine: Instance of QnAEngine
        host: Host address to run the server on
        port: Port number to run the server on
        debug: Whether to run in debug mode
    """
    global db_manager, qna_engine
    db_manager = database_manager
    qna_engine = qa_engine
    
    logger.info(f"Starting web interface on {host}:{port}")
    app.run(host=host, port=port, debug=debug)

# Server configuration
if __name__ == '__main__':
    from database.database_manager import DBManager
    from llm.qna_engine import QnAEngine
    
    db_manager = DBManager()
    qna_engine = QnAEngine()
    
    run_web_app(db_manager, qna_engine, debug=True)