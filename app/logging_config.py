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
File: app/logging_config.py
Author: Hosu Kim
Created: 2025-03-22 13:07:26 UTC

Description:
    Configuration for the application's logging system.'
'''

import os
from datetime import datetime
import logging
import logging.handlers

def setup_logging(debug_mode=False, console_logs=True):
    """
    Configure the logging system.

    Args:
        debug_mode (bool): If True, enables more detailed debug logging
        console_logs (bool): If True, logs will be output to console. If False, logs only to file
    """
    # Create log directory if it doesn't exist
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Set log file name with current date
    log_filename = os.path.join(log_dir, f"goal_talk{datetime.now().strftime('%Y%m%d')}.log")

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG if debug_mode else logging.INFO)

# Uses slice notation [:] to create a copy of the handlers list for safe iteration
# This prevents index shifting issues when removing handlers during iteration
#
# Example problem without slice notation:
# handlers = ["h1", "h2", "h3"]
# for h in handlers: handlers.remove(h)
#   Iteration 1: h = "h1" -> remove "h1" -> handlers = ["h2", "h3"]
#   Iteration 2: h = "h3" -> remove "h3" -> handlers = ["h2"]
#   Iteration ends with ["h2"] still in the list! "h2" is never processed.
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Configure file handler
    file_handler = logging.handlers.RotatingFileHandler(
        log_filename,
        maxBytes=10*1024*1024, # 10MB
        backupCount=5,
        encoding="utf-8"
    )
    file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(file_formatter)
    root_logger.addHandler(file_handler)

    # Configire console handler (optional)
    if console_logs:
        console_handler = logging.StreamHandler()
        console_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        console_handler.setFormatter(console_formatter)
        root_logger.addHandler(console_handler)

    # This prevents HTTP client libraries from flooding logs with debug information
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)

    # Log initialization message
    if debug_mode:
        logging.debug("Debug logging enabled")

    logging.info(f"Logging initialized. Log file: {log_filename}")

    return root_logger