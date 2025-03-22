# goAI Talk - Football Match Results Q&A Bot
## Overview
goAI Talk is an interactive Football Match Results Q&A Bot that provides detailed information about yesterday's football matches. The system allows users to query match results, scores, team performance, and other football statistics through both a CLI and web interface.
## Features
- **Rich Q&A Capabilities**: Ask natural language questions about football matches
- **Dual Interfaces**: Choose between CLI or web interface
- **Data Coverage**:
	- Match results and scores
	- Team statistics
	- League information
	- Venue details
	- Goal details
	- Country information
- **Rich Text Formatting**: Clean, structured responses with proper alignment
- **Example Questions**: Built-in question suggestions to help users get started
- **Comprehensive Logging**: Detailed logs for debugging and monitoring
## Prerequisites
- Python 3.10 or higher
- API credentials:
	- Football API key (from API-Football)
	- OpenAI API key (for Q&A functionality)
- Internet connection for API data updates
## Installation
### Local Setup
1. Clone the repository:
```bash
git clone https://github.com/hosu-kim/goAI_talk.git
```
```bash
cd goAI_talk
```
2. Install dependencies:
```bash
pip install -r requirements.txt
```
### Docker Setup
1. Build the Docker image:
```bash
docker build -t goai-talk .
```
2. Run the container:
```bash
docker run -it -p 8000:8000 -v goai-data:/app/data goai-talk
```
## Usage
### Command Line Interface
Run the application and choose the CLI option:
```bash
python3 main.py
```
When prompted, select option 1 for CLI interface.
**CLI Commands:**
- Type your question about yesterday's football matches
- `help` - Display example questions
- `info` - Show information about available data
- `update` - Update database with latest match data
- `exit` or `quit` - End the session
### Web Interface
Run the application and choose the web interface option:
```bash
python3 main.py
```
When prompted, select option 2 for Web Interface.
Then, open your browser and navigate to:
http://localhost:8000
### Example Questions
- "What were yesterday's match results?"
- "How many matches ended in a home win?"
- "Which teams kept a clean sheet yesterday?"
- "Which match had the highest score?"
- "What was the halftime score in the CSA match?"
- "Show me all CONCACAF Champions League matches"
- "Did Inter Miami win their match?"
- "Which matches were played in Brazil?"
## Data Updates
To update the database with the latest match data:
```bash
python main.py --update
```
## Project Structure
```code
goAI_talk/
├── app/
│   ├── __init__.py              # Package initialization
│   ├── api.py                   # Football API interaction
│   ├── cli_interface/           # Command-line interface
│   │   ├── __init__.py
│   │   └── cli.py
│   ├── config/                  # Configuration files
│   │   ├── __init__.py
│   │   └── example_questions.py # Example questions for users
│   ├── database_manager/        # Database operations
│   │   ├── database.py
│   │   └── football_data.db     # SQLite database
│   ├── domain/                  # Domain models
│   │   └── domain.py            # Contains Match and other domain classes
│   ├── exceptions.py            # Custom exceptions
│   ├── llm.py                   # LLM integration for Q&A
│   ├── logging_config.py        # Logging configuration
│   ├── models.py                # Data models
│   └── web_interface/           # Web interface
│       ├── __init__.py
│       ├── static/              # CSS and JavaScript
│       │   ├── scripts.js
│       │   └── styles.css
│       ├── templates/           # HTML templates
│       │   ├── examples.html
│       │   └── index.html
│       └── web.py
├── config.py                    # Configuration settings
├── logs/                        # Log file directory
│   └── goal_talk*.log           # Log files
├── main.py                      # Application entry point
├── requirements.txt             # Dependencies
├── tests/                       # Test files
│   ├── test_api.py
│   └── test_data.json
├── Dockerfile                   # Docker configuration
└── README.md                    # This file
```
## Test Mode
Uses predefined data from tests/test_data.json instead of API calls
```bash
python main.py --test
```
## Debug Mode
Enablee verbose logging for debugging
```bash
python3 main.py --debug
```
## Console Logging
Display logs in the console (by default logs are only saved to files)
```bash
python3 main.py --log-console
```
## Combined Options
Options can be combined as needed:
```bash
python3 main.py --debg --log-console --test
```
## Troubleshooting
- No match data available: Run with the `--update` flag to fetch new data
- API connection issues: Verify your internet connection and API keys
- Database errors: Check if the database file exists and has write permissions
- Log files: Check logs/ directory for detailed application logs