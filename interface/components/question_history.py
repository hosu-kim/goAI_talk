# interface/components/question_history.py

import json
import os
from datetime import datetime
from rich.table import Table

class QuestionHistory:
	"""사용자 질문 기록 관리"""
	
	def __init__(self, history_file="question_history.json"):
		"""
		질문 기록 관리자 초기화
		
		Args:
			history_file (str): 질문 기록 파일 경로
		"""
		self.history_file = history_file
		self.history = self._load_history()
		
	def _load_history(self):
		"""기록 파일에서 질문 내역 로드"""
		if os.path.exists(self.history_file):
			try:
				with open(self.history_file, 'r') as f:
					return json.load(f)
			except:
				return []
		return []
	
	def _save_history(self):
		"""질문 내역 파일로 저장"""
		with open(self.history_file, 'w') as f:
			json.dump(self.history, f, indent=2)
	
	def add_question(self, question, answer=None):
		"""
		새 질문 추가
		
		Args:
			question (str): 사용자 질문
			answer (str, optional): 시스템 응답
		"""
		self.history.append({
			"timestamp": datetime.utcnow().isoformat(),
			"question": question,
			"answer": answer
		})
		
		# 최대 100개 질문만 유지
		if len(self.history) > 100:
			self.history = self.history[-100:]
			
		self._save_history()
	
	def get_recent_questions(self, count=5):
		"""
		최근 질문 가져오기
		
		Args:
			count (int): 가져올 질문 수
		
		Returns:
			list: 최근 질문 목록
		"""
		return self.history[-count:]
	
	def create_history_table(self, count=5):
		"""
		최근 질문 기록 테이블 생성
		
		Args:
			count (int): 표시할 질문 수
			
		Returns:
			Table: Rich 테이블 객체
		"""
		table = Table(title="Recent Questions")
		table.add_column("Time", style="dim")
		table.add_column("Question", style="cyan")
		
		recent = self.get_recent_questions(count)
		
		if not recent:
			table.add_row("N/A", "No previous questions")
			return table
		
		for item in reversed(recent):
			# ISO 형식 시간을 가독성 있게 변환
			timestamp = item.get("timestamp", "")
			try:
				dt = datetime.fromisoformat(timestamp)
				time_str = dt.strftime("%H:%M:%S")
			except:
				time_str = "Unknown"
				
			question = item.get("question", "")
			# 질문이 너무 길면 잘라내기
			if len(question) > 50:
				question = question[:47] + "..."
				
			table.add_row(time_str, question)
			
		return table
	
	def search_questions(self, keyword):
		"""
		키워드로 질문 검색
		
		Args:
			keyword (str): 검색할 키워드
			
		Returns:
			list: 검색 결과 목록
		"""
		keyword = keyword.lower()
		results = []
		
		for item in self.history:
			question = item.get("question", "").lower()
			if keyword in question:
				results.append(item)
				
		return results
	
	def clear_history(self):
		"""질문 기록 초기화"""
		self.history = []
		self._save_history()