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
File: interface/components/help_menu.py
Author: hosu-kim
Created: 2024-03-14

Description:
    This module provides functionality to create and display the help menu
    in the CLI interface using Rich library components.
"""
from rich.panel import Panel
from rich.markdown import Markdown

def create_help_menu(console):
    """Creates a formatted help menu panel.
    
    Generates a comprehensive help menu showing available commands
    and example questions that users can ask the system.
    
    Args:
        console (Console): Rich console object for display
        
    Returns:
        Panel: A Rich Panel containing formatted help information
    """
    help_text = """
    # Football Q&A Bot - Help Menu

    ## Available Commands

    * `help` - Show this help message
    * `exit`, `quit`, `q` - Exit the application
    * `refresh`, `update` - Refresh match data from API
    * `leagues`, `competitions` - Show available leagues
    * `teams` - Show available teams
    * `matches` - Show summary of yesterday's matches
    * `stats` - Show match statistics

    ## Example Questions

    * "Who won the Premier League match yesterday?"
    * "Did Manchester United play yesterday?"
    * "How many goals were scored in La Liga?"
    * "Who scored for Arsenal?"
    * "Which team had the most goals yesterday?"
    * "Show me the results from Serie A"
    """
    
    md = Markdown(help_text)
    return Panel(md, title="Help", border_style="blue", width=80)
