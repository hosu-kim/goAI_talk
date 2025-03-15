```code
football-qa/
│
├── app/
│   ├── __init__.py
│   ├── api.py                 # API-Football integration
│   ├── database.py            # SQLite database management
│   ├── models.py              # Data model definitions
│   ├── llm.py                 # OpenAI integration and Q&A processing
│   ├── cli.py                 # CLI interface
│   └── web.py                 # Web interface (FastAPI)
│
├── static/                    # Web interface static files
│   ├── style.css
│   └── script.js
│
├── templates/                 # Web interface templates
│   └── index.html
│
├── main.py                    # Application entry point
├── config.py                  # Configuration management (API keys, DB settings)
├── requirements.txt           # Dependencies list
├── Dockerfile                 # Docker configuration
└── README.md                  # Project documentation
```
