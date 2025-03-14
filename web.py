#!/usr/bin/env python3
"""
Web interface launcher for the Football Q&A Bot.
This is a simple wrapper that makes it easier to run the web interface.
"""

from interface.web import app, run_web_app
from database.database_manager import DBManager
from llm.qna_engine import QnAEngine

if __name__ == "__main__":
    print("Starting Football Q&A Bot Web Interface...")
    db_manager = DBManager()
    qna_engine = QnAEngine()
    
    # Run the web interface
    run_web_app(db_manager, qna_engine, debug=True)
