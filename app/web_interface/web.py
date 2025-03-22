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
import logging
from typing import List, Optional, Tuple, Union
from datetime import datetime

# Add parent dir to sys.path to import other modules in the other dirs
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse

from config import settings
from app.config.example_questions import EXAMPLE_QUESTIONS
from app.database_manager.database import Database
from app.llm import QnAEngine
from app.domain.domain import Match
from app.exceptions import DataProcessingError, APIConnectionError

# Get a logger for this module
logger = logging.getLogger(__name__)

app: FastAPI = FastAPI(title="goAI Talk")
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "templates"))
app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "static")), name="static")

# Dependency injection: QnAEngine and Database are created using settings.
db: Database = Database(settings)
qna_engine: QnAEngine = QnAEngine(settings, db)

# Format current time in the user time zone.
CURRENT_TIME: str = datetime.today().strftime("%Y-%m-%d %H:%M:%S")

_match_cache = {
    "last_updated": None,
    "matches": None,
    "date": "yesterday",
    "count": 0
}

def get_match_context() -> Tuple[str, int]:
    """
    Fetch match data one and return the match date and match count.
    Uses caching to avoid multiple database calls within the same request cycle.

    The cache is refreshed every 5 minutes (300 seconds) to ensure data
    stays reasonably current while reducing database load.

    Returns:
        Tuple[str, int]: The match date and the total count of matches.
    """
    # Check if cache needs to be initialized or refreshed
    current_time = datetime.now()
    if (_match_cache["last_updated"] is None or
        (current_time - _match_cache["last_updated"]).total_seconds() > 300):

        logger.debug("Match context cache expired, refreshing from database")
        all_matches: List[Match] = db.retrieve_yesterdays_matches_from_db()

        _match_cache["matches"] = all_matches
        _match_cache["count"] = len(all_matches)
        _match_cache["last_updated"] = current_time

        if all_matches and len(all_matches) > 0:
            _match_cache["date"] = all_matches[0].date
    
        logger.debug(f"Updated match context cache: date={_match_cache['date']}, count={_match_cache['count']}")
    else:
        logger.debug("Using cached match context data")
    
    return _match_cache["date"], _match_cache["count"]

@app.get("/", response_class=HTMLResponse)
async def index(request: Request, prefill: Optional[str] = None) -> HTMLResponse:
    """Renders the main page of the application."""
    logger.info(f"GET / - IP: {request.client.host}")
    match_date, match_count = get_match_context()

    logger.debug(f"Rendering index with prefill={prefill}")
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
    logger.info(f"POST /ask - IP: {request.client.host}, Question: '{question}'")

    if not question.strip():
        logger.warning("Empty question submitted, redirecting to home page")
        return RedirectResponse(url="/", status_code=303)

    match_date, match_count = get_match_context()

    try:
        logger.debug(f"Processing question: '{question}'")
        answer: str = qna_engine.get_answer(question)

        truncated_answer = answer[:100] + "..." if len(answer) > 10 else answer
        logger.debug(f"Answer generated: '{truncated_answer}'")

    except Exception as e:
        if isinstance(e, DataProcessingError):
            logger.error(f"Data processing error: {str(e)}", exc_info=True)
            answer = f"Sorry, I encountered an error processing match data: {str(e)}"
        elif isinstance(e, APIConnectionError):
            logger.error(f"API connection error: {str(e)}", exc_info=True)
            answer = f"Sorry, I couldn't connect to the AI service. Please try again later."
        else:
            logger.erro(f"Unexpected error: {type(e).__name__}: {str(e)}", exc_info=True)
            answer = f"An unexpected error occurred. Please try asking another question."

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
    logger.info(f"GET /examples - IP: {request.client.host}")
    return templates.TemplateResponse(
        "examples.html",
        {
            "request": request,
            "examples": EXAMPLE_QUESTIONS,
            "current_time": CURRENT_TIME
        }
    )

@app.get("/favicon.ico")
async def favicon() -> RedirectResponse:
    """Handles favicon.ico requests."""
    return RedirectResponse(url="/static/favicon.ico")

def run_server(host: str="0.0.0.0", port: int = 8000) -> None:
    """Starts the FastAPI web server."""
    logger.info(f"Starting web server on {host}:{port}")
    uvicorn.run(app, host=host, port=port)

if __name__ == "__main__":
    run_server()
