from datetime import datetime, timedelta
import os
import pytz

def get_current_time(format_str="%Y-%m-%d %H:%M:%S", timezone=None):
	"""
	현재 시간을 지정된 형식과 시간대로 반환
	
	Args:
		format_str (str): 날짜/시간 형식
		timezone (str): 시간대 (기본값은 환경 변수 또는 UTC)
		
	Returns:
		str: 포맷된 현재 시간
	"""
	if timezone is None:
		timezone = os.getenv("USER_TIMEZONE", "UTC")
		
	try:
		tz = pytz.timezone(timezone)
		return datetime.now(tz).strftime(format_str)
	except Exception:
		# 시간대 오류 시 UTC 사용
		return datetime.utcnow().strftime(format_str)

def get_yesterday_date(format_str="%Y-%m-%d", timezone=None):
	"""
	어제 날짜를 지정된 형식으로 반환
	
	Args:
		format_str (str): 날짜 형식
		timezone (str): 시간대 (기본값은 환경 변수 또는 UTC)
		
	Returns:
		str: 포맷된 어제 날짜
	"""
	if timezone is None:
		timezone = os.getenv("USER_TIMEZONE", "UTC")
		
	try:
		tz = pytz.timezone(timezone)
		yesterday = datetime.now(tz) - timedelta(days=1)
		return yesterday.strftime(format_str)
	except Exception:
		# 시간대 오류 시 UTC 사용
		yesterday = datetime.utcnow() - timedelta(days=1)
		return yesterday.strftime(format_str)

def get_user_info():
	"""
	현재 사용자 정보 조회
	
	Returns:
		dict: 사용자 이름, 로그인 시간, 시간대 등
	"""
	import getpass
	
	username = os.getenv("USER", getpass.getuser())
	return {
		"username": username,
		"login_time": get_current_time(),
		"timezone": os.getenv("USER_TIMEZONE", "UTC")
	}