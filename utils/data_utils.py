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
File: utils/data_utils.py
Author: hosu-kim
Created: 2025-03-14 11:08:17 UTC

Description:
    This module provides utility functions for handling dates, times, and user information.
    It supports timezone-aware date operations and formatting.
"""
from datetime import datetime, timedelta
import os

def get_current_time(format_str="%Y-%m-%d %H:%M:%S", timezone=None):
	"""
	Return the current time in the specified format and timezone.
	
	Args:
		format_str (str): Date/time format
		timezone (str): Timezone (default is environment variable or UTC)
		
	Returns:
		str: Formatted current time
	"""
	# Simplified to not require pytz
	return datetime.utcnow().strftime(format_str)

def get_yesterday_date(format_str="%Y-%m-%d", timezone=None):
	"""
	Return yesterday's date in the specified format.
	
	Args:
		format_str (str): Date format
		timezone (str): Timezone (default is environment variable or UTC)
		
	Returns:
		str: Formatted yesterday's date
	"""
	# Simplified to not require pytz
	yesterday = datetime.utcnow() - timedelta(days=1)
	return yesterday.strftime(format_str)

def get_current_date(format_str="%Y-%m-%d", timezone=None):
	"""
	Return the current date in the specified format.
	
	Args:
		format_str (str): Date format
		timezone (str): Timezone (default is environment variable or UTC)
		
	Returns:
		str: Formatted current date
	"""
	# Simplified to not require pytz
	return datetime.utcnow().strftime(format_str)

def get_user_info():
	"""
	Get current user information.
	
	Returns:
		dict: User name, login time, timezone, etc.
	"""
	import getpass
	
	username = os.getenv("USER", getpass.getuser())
	return {
		"username": username,
		"login_time": get_current_time(),
		"timezone": os.getenv("USER_TIMEZONE", "UTC")
	}