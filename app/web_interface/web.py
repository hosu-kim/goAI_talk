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
File: app/web_interface/web.py
Author: Hosu Kim
Created: 2025-03-15 20:07:06 UTC

Description:
    Web server module for goAI_talk. 
    Implements a FastAPI-based web interface for user interaction, 
    handling HTTP requests and serving HTML responses
    with football match Q&A functionality.
'''

import os
import sys
import uvicorn
from typing import Dict, List, Optional, Any, Union
from datetime import datetime

# Add parent dir to sys.path to import other modules in the other dirs
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse

from config import settings
from app.database_manager.database import Database
from app.llm import QnAEngine


app: FastAPI = FastAPI(title="goAI Talk")
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "templates"))
app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "static")), name="static")

qna_engine: QnAEngine = QnAEngine(settings)
db: Database = Database(settings)

# Format current time in the user time zone.
CURRENT_TIME: str = datetime.today().strftime("%Y-%m-%d %H:%M:%S")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request, prefill: Optional[str] = None) -> HTMLResponse:
    """Renders the main page of the application."""
    matches: List[Dict[str, Any]] = db.retrieve_yesterdays_matches_from_db(max_matches=1)
    match_date: str = "yesterday"
    match_count: int = 0
    
    if matches and len(matches) > 0:
        match_date = matches[0]['date']
        all_matches: List[Dict[str, Any]] = db.retrieve_yesterdays_matches_from_db()
        match_count = len(all_matches)
    
    return templates.TemplateResponse(
        "index.html", 
        {
            "request": request,
            "match_date": match_date,
            "match_count": match_count,
            "current_time": CURRENT_TIME,
            "prefill": prefill
        }
    )

@app.post("/ask", response_class=HTMLResponse, response_model=None)
async def ask(request: Request, question: str = Form(...)) -> Union[HTMLResponse, RedirectResponse]:
    """Processes user questions about football matches."""
    if not question.strip():
        return RedirectResponse(url="/", status_code=303)
        
    matches: List[Dict[str, Any]] = db.retrieve_yesterdays_matches_from_db(max_matches=1)
    match_date: str = "yesterday"
    match_count: int = 0
    
    if matches and len(matches) > 0:
        match_date = matches[0]['date']
        all_matches: List[Dict[str, Any]] = db.retrieve_yesterdays_matches_from_db()
        match_count = len(all_matches)
    
    try:
        answer: str = qna_engine.get_answer(question)
    except Exception as e:
        answer = f"Sorry, I encountered an error. Please try asking another question."
    
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request, 
            "question": question, 
            "answer": answer,
            "match_date": match_date,
            "match_count": match_count,
            "current_time": CURRENT_TIME
        }
    )

@app.get("/examples", response_class=HTMLResponse)
async def examples(request: Request) -> HTMLResponse:
    """Provides example questions based on available match data."""
    examples: Dict[str, List[str]] = {
        "Match Results": [
            "What were yesterday's match results?",
            "How many matches ended in a home win?",
            "Which teams kept a clean sheet yesterday?"
        ],
        "Score Details": [
            "Which match had the highest score?",
            "What was the halftime score in the CSA match?",
            "Were there any matches that went to extra time?"
        ],
        "League Information": [
            "Show me all CONCACAF Champions League matches",
            "What matches were played in the Copa Do Brasil?",
            "How many different leagues had matches yesterday?"
        ],
        "Venue & Location": [
            "Which matches were played in Brazil?",
            "What matches were played at Independence Park?",
            "Show me all match venues and their cities"
        ],
        "Team Performance": [
            "Did Inter Miami win their match?",
            "Which team scored the most goals in a single match?",
            "Show me all matches where the home team won"
        ]
    }
    
    return templates.TemplateResponse(
        "examples.html", 
        {
            "request": request,
            "examples": examples,
            "current_time": CURRENT_TIME
        }
    )

@app.get("/favicon.ico")
async def favicon() ->RedirectResponse:
    """Handles favicon.ico requests."""
    return RedirectResponse(url="/static/favicon.ico")

def run_server(host: str="0.0.0.0", port: int = 8000) -> None:
    """Starts the FastAPI web server."""
    uvicorn.run(app, host=host, port=port)

if __name__ == "__main__":
    run_server()
