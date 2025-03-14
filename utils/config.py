import os
import logging
from dotenv import load_dotenv

def load_config():
	"""환경 변수 로딩 및 구성 설정"""
	load_dotenv()
	
	config = {
		# API 키
		"football_api_key": os.getenv("FOOTBALL_API_KEY"),
		"openai_api_key": os.getenv("OPENAI_API_KEY"),
		
		# 애플리케이션 설정
		"debug": os.getenv("DEBUG", "False").lower() == "true",
		"log_level": os.getenv("LOG_LEVEL", "INFO").upper(),
		"user_timezone": os.getenv("USER_TIMEZONE", "UTC"),
		"max_matches": int(os.getenv("MAX_MATCHES", "30")),
		"openai_model": os.getenv("OPENAI_MODEL", "gpt-3.5-turbo"),
		
		# 데이터베이스 설정
		"db_dir": os.getenv("DB_DIR", "database"),
		"db_name": os.getenv("DB_NAME", "football_matches.db"),
	}
	
	# DB 경로 완성
	config["db_path"] = os.path.join(config["db_dir"], config["db_name"])
	
	# 로그 레벨 설정
	log_levels = {
		"DEBUG": logging.DEBUG,
		"INFO": logging.INFO,
		"WARNING": logging.WARNING,
		"ERROR": logging.ERROR,
		"CRITICAL": logging.CRITICAL
	}
	config["log_level_enum"] = log_levels.get(config["log_level"], logging.INFO)
	
	return config

def setup_logger(name, log_dir="logs"):
	"""로거 설정 통합 함수"""
	config = load_config()
	
	os.makedirs(log_dir, exist_ok=True)
	log_file = os.path.join(log_dir, f"{name}.log")
	
	logger = logging.getLogger(name)
	logger.setLevel(config["log_level_enum"])
	
	# 기존 핸들러가 없을 때만 추가
	if not logger.handlers:
		# 파일 핸들러
		file_handler = logging.FileHandler(log_file)
		file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
		file_handler.setFormatter(file_formatter)
		logger.addHandler(file_handler)
		
		# 디버그 모드에서만 콘솔 핸들러 추가
		if config["debug"]:
			console_handler = logging.StreamHandler()
			console_formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
			console_handler.setFormatter(console_formatter)
			logger.addHandler(console_handler)
	
	return logger