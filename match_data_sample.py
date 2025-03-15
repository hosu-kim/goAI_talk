import requests
from datetime import datetime, timedelta
import json

# 어제 날짜 계산
yesterday = datetime.now() - timedelta(1)
yesterday_str = yesterday.strftime('%Y-%m-%d')  # 어제 날짜를 'YYYY-MM-DD' 형식으로

# API URL 설정 (예시: 스포츠 데이터 API)
url = f'https://www.thesportsdb.com/api/v1/json/3/eventsday.php?d=2025-03-15'

# API 요청 보내기
response = requests.get(url)

# 응답이 성공적이면 JSON으로 저장
if response.status_code == 200:
    data = response.json()

    # JSON 파일로 저장
    with open('yesterday_sports_data.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)

    print("JSON 파일로 저장되었습니다.")
else:
    print(f"API 요청 실패: {response.status_code}")
