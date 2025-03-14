#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
File: llm/response_cache.py
Author: hosu-kim
Created: 2025-03-14 12:10:22 UTC

Description:
    This module provides caching functionality for LLM responses.
    It reduces API calls by caching responses based on questions and data hashes.
"""
import hashlib
import os
import json
import pickle
from datetime import datetime, timedelta
from utils.config import setup_logger

class ResponseCache:
	"""
	LLM 응답 캐싱 시스템
	질문과 데이터 기반으로 응답을 캐싱하여 API 호출 감소
	"""
	def __init__(self, cache_dir="cache", ttl_hours=24):
		"""
		응답 캐싱 시스템 초기화
		
		Args:
			cache_dir (str): 캐시 저장 디렉토리
			ttl_hours (int): 캐시 유효 기간(시간)
		"""
		self.cache_dir = cache_dir
		os.makedirs(cache_dir, exist_ok=True)
		self.ttl = timedelta(hours=ttl_hours)
		self.logger = setup_logger("cache")
		
	def _get_cache_key(self, question, data_hash):
		"""캐시 키 생성"""
		combined = f"{question.lower().strip()}:{data_hash}"
		return hashlib.md5(combined.encode()).hexdigest()
	
	def _get_data_hash(self, data):
		"""데이터 해시 생성"""
		# 핵심 정보만 추출하여 해시 생성
		simplified = []
		for item in data:
			simple_item = {
				"id": item.get("id", ""),
				"home": item.get("home_team", ""),
				"away": item.get("away_team", ""),
				"score": f"{item.get('home_score', 0)}-{item.get('away_score', 0)}",
			}
			simplified.append(simple_item)
			
		data_str = json.dumps(simplified, sort_keys=True)
		return hashlib.md5(data_str.encode()).hexdigest()
	
	def get(self, question, data):
		"""
		캐시된 응답 조회
		
		Args:
			question (str): 사용자 질문
			data (list): 매치 데이터
			
		Returns:
			str or None: 캐시된 응답 또는 None
		"""
		try:
			data_hash = self._get_data_hash(data)
			cache_key = self._get_cache_key(question, data_hash)
			cache_file = os.path.join(self.cache_dir, f"{cache_key}.pkl")
			
			if os.path.exists(cache_file):
				with open(cache_file, 'rb') as f:
					cache_data = pickle.load(f)
				
				# 캐시 유효기간 확인
				if datetime.utcnow() - cache_data['timestamp'] < self.ttl:
					self.logger.info(f"Cache hit for question: {question[:30]}...")
					return cache_data['response']
				else:
					self.logger.info(f"Cache expired for question: {question[:30]}...")
					
		except Exception as e:
			self.logger.error(f"Error retrieving cache: {str(e)}", exc_info=True)
			
		return None
	
	def set(self, question, data, response):
		"""
		응답 캐싱
		
		Args:
			question (str): 사용자 질문
			data (list): 매치 데이터
			response (str): LLM 응답
		"""
		try:
			data_hash = self._get_data_hash(data)
			cache_key = self._get_cache_key(question, data_hash)
			cache_file = os.path.join(self.cache_dir, f"{cache_key}.pkl")
			
			cache_data = {
				'timestamp': datetime.utcnow(),
				'response': response,
				'question': question
			}
			
			with open(cache_file, 'wb') as f:
				pickle.dump(cache_data, f)
				
			self.logger.info(f"Cached response for question: {question[:30]}...")
		except Exception as e:
			self.logger.error(f"Error caching response: {str(e)}", exc_info=True)