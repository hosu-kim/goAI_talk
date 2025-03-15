"""Common constants used throughout the application"""
import logging

# OpenAI API defaults
DEFAULT_MODEL = "gpt-3.5-turbo"
DEFAULT_TEMPERATURE = 0.7
DEFAULT_MAX_TOKENS = 200

# API request settings
DEFAULT_API_TIMEOUT = 30  # seconds
DEFAULT_RETRY_COUNT = 3

# Data settings
DEFAULT_CACHE_DURATION = 21600  # 6 hours in seconds

# Logging levels mapping
LOG_LEVELS = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL
}
