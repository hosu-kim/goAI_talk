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
File: README.md
Author: Hosu Kim
Created: 2024-03-14 12:10:22 UTC

Description:
    Main documentation file for the goAI_talk project.
    Contains setup instructions, usage guidelines, and project overview.
"""

# Football Match Results Q&A Bot 🤖⚽

An intelligent assistant powered by GPT that provides natural language interaction for querying football match results and statistics.

## Overview

This bot leverages natural language processing to help users get information about football matches through simple conversations. It supports both command-line and web interfaces, making it versatile for different use cases.

## Key Features

- 🗣️ **Natural Language Understanding**: Ask questions in plain English about matches, scores, and players
- 📊 **Comprehensive Match Data**: Access detailed match statistics, scores, and goal information
- ⚽ **Goal Details**: Get information about scorers, timing, and types of goals
- 🏆 **League Filtering**: Filter and focus on specific leagues or competitions
- 💻 **Dual Interface**: Choose between CLI for efficiency or Web UI for convenience
- 🔄 **Real-time Updates**: Fetch latest match data with simple refresh command
- 📱 **Responsive Design**: Web interface works seamlessly on both desktop and mobile

## Getting Started

### Prerequisites

- Python 3.9 or higher
- API Keys:
  - Football API ([api-sports.io](https://api-sports.io))
  - OpenAI API ([platform.openai.com](https://platform.openai.com))
- pip (Python package installer)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/football-qna-bot.git
cd football-qna-bot
```

2. Create and activate virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
cp .env.example .env
# Edit .env file with your API keys
```

## Usage Guide

### Command-Line Interface (CLI)

1. Start the bot:
```bash
python main.py
```

2. Fetch latest match data:
```bash
python main.py --fetch
```

3. Available commands:
- `help` - Display help information
- `leagues` - Show available leagues
- `matches` - Display all matches
- `refresh` - Update match data
- `exit` - Close application

### Web Interface

1. Start the web server:
```bash
python main.py --web
```

2. Access the interface:
- Open `http://localhost:8000` in your browser
- Use the search bar to ask questions
- Filter matches by league using the dropdown

### Example Questions

```
Q: "Who won the Manchester United game yesterday?"
Q: "How many goals were scored in the Premier League?"
Q: "Show me all matches from La Liga"
Q: "Who scored for Arsenal?"
```

## Configuration

Customize the bot's behavior through `config.json`:

```json
{
  "language": "en",
  "default_timezone": "UTC",
  "max_cache_age_hours": 12,
  "preferred_leagues": [
    "Premier League",
    "La Liga",
    "Serie A",
    "Bundesliga",
    "Ligue 1"
  ],
  "max_results": 10
}
```

## Docker Deployment

1. Build the container:
```bash
docker build -t football-qna-bot .
```

2. Run the application:
```bash
# CLI mode
docker run -it football-qna-bot

# Web mode
docker run -p 8000:8000 football-qna-bot --web
```

## Docker 배포 가이드

### 사전 요구사항
- Docker 및 Docker Compose 설치
- API 키 설정 (.env 파일에 저장)

### Docker로 실행하기

1. Docker 이미지 빌드:
```bash
docker-compose build
```

2. Docker 컨테이너 실행:
```bash
# 웹 인터페이스로 실행
docker-compose up

# 백그라운드로 실행
docker-compose up -d
```

3. CLI 모드로 실행:
```bash
# docker-compose.yml의 command 부분을 수정하거나
# 아래 명령어로 직접 실행
docker-compose run --rm football-qa-bot python main.py
```

4. 데이터 갱신:
```bash
docker-compose run --rm football-qa-bot python main.py --fetch
```

5. 컨테이너 중지:
```bash
docker-compose down
```

### Docker 환경 변수

Docker Compose 파일에서 다음과 같은 환경 변수를 설정할 수 있습니다:

- `DEBUG`: 디버그 모드 활성화 (True/False)
- `LOG_LEVEL`: 로그 레벨 (INFO, DEBUG, WARNING, ERROR, CRITICAL)
- `LOG_DIR`: 로그 저장 디렉토리
- `USER_TIMEZONE`: 사용자 타임존 (기본값: UTC)

### Docker 볼륨

다음 볼륨들이 마운트됩니다:

- `./logs`: 애플리케이션 로그 파일
- `./database`: SQLite 데이터베이스 파일
- `./cache`: 캐시 데이터

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) file for details.

## Acknowledgments

- [API-Football](https://www.api-football.com/) for match data
- [OpenAI](https://openai.com/) for natural language processing
- [Rich](https://github.com/Textualize/rich) for terminal formatting

## Support

- 📫 Report issues on GitHub
- 📝 Contribute to documentation
- 🤝 Submit pull requests
- 💬 Join discussions

---
Created with ❤️ by [Hosu Kim](https://github.com/hosu-kim)
