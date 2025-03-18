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
- **Rich Text Formatting**: Clean, structured responses with proper alignment
- **Example Questions**: Built-in question suggestions to help users get started
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
docker run -p 8000:8000 \
  -e API_FOOTBALL_KEY=your_football_api_key_here \
  -e OPENAI_API_KEY=your_openai_api_key_here \
  -v goai-data:/app/data \
  goai-talk
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
│   ├── api.py                   # Football API interaction
│   ├── cli_interface/           # Command-line interface
│   │   └── cli.py
│   ├── database_manager/        # Database operations
│   │   ├── database.py
│   │   └── football_data.db     # SQLite database
│   ├── llm.py                   # LLM integration for Q&A
│   └── web_interface/           # Web interface
│       ├── static/              # CSS and JavaScript
│       ├── templates/           # HTML templates
│       └── web.py
├── config.py                    # Configuration settings
├── main.py                      # Application entry point
├── requirements.txt             # Dependencies
├── tests/                       # Test files
├── Dockerfile                   # Docker configuration
└── README.md                    # This file
```
## Docker Recommendations
The included Dockerfile can be enhanced with the following improvements:
```Dockerfile
FROM python:3.10-slim

# Create a non-root user
RUN useradd -m appuser

WORKDIR /app

# Copy and install dependencies first (for better caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create data directory and set permissions
RUN mkdir -p /app/data && chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Volume for storing database files
VOLUME /app/data

# Set environment variables
ENV DB_PATH=/app/data/football_data.db
# Note: API keys should be provided at runtime

# Expose the web server port
EXPOSE 8000

# Run web interface by default (modified to match your application)
CMD ["python3", "main.py", "--update"]
```
## Troubleshooting
- No match data available: Run with the `--update` flag to fetch new data
- API connection issues: Verify your internet connection and API keys
- Database errors: Check if the database file exists and has write permissions