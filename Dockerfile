# 베이스 이미지로 Python 3.9 사용
FROM python:3.9-slim

# 작업 디렉토리 설정
WORKDIR /app

# 패키지 의존성 설치를 위한 파일 먼저 복사
COPY requirements.txt .

# 필요한 시스템 패키지 설치 및 Python 패키지 설치
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get purge -y --auto-remove gcc && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 애플리케이션 코드 복사
COPY . .

# 필요한 디렉토리 생성
RUN mkdir -p logs database cache

# 8000번 포트 노출
EXPOSE 8000

# 환경 변수 설정
ENV PYTHONUNBUFFERED=1

# 실행 명령어 (인자는 docker-compose에서 오버라이드 가능)
CMD ["python", "main.py"]