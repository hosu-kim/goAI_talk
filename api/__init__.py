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
File: api/__init__.py
Author: hosu-kim
Created: 2025-03-14 09:39:46 UTC

Description:
    API package initialization for goAI_talk application.
    This package contains modules for interacting with external
    football data APIs and services.
"""

# API package version
__version__ = '1.0.0'

# List of modules to expose when using "from api import *"
__all__ = ['football_api']

# Define package-level constants
API_TIMEOUT = 30  # Default timeout for API requests in seconds
DEFAULT_CACHE_EXPIRY = 3600  # Default cache expiry time in seconds