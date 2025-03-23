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
File: app/exceptions.py
Author: Hosu Kim
Created: 2025-03-21 12:06:03 UTC

Description:
    This module defines `custom exceptions` for the football API client.
'''

class FootballAPIError(Exception):
    """Base exception for Football API related errors."""
    pass

class APIConnectionError(FootballAPIError):
    """Raised when there's an error connecting to the API.

    Examples:
        - Non-200 status code
        - Invalid JSON format in response
        - Missing required fields in response
    """
    pass

class APIResponseError(FootballAPIError):
    """Raised when the API returns an unexpected response."""
    pass

class DataProcessingError(FootballAPIError):
    """Raised when there's an error processing API data."""
    pass