// Football Matches Q&A Bot 클라이언트 스크립트
document.addEventListener('DOMContentLoaded', function() {
	// 질문 폼 제출 시 로딩 표시
	const questionForm = document.getElementById('questionForm');
	if (questionForm) {
		questionForm.addEventListener('submit', function() {
			const submitBtn = this.querySelector('button[type="submit"]');
			submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Processing...';
			submitBtn.disabled = true;
		});
	}
	
	// 매치 필터링
	const leagueFilter = document.getElementById('leagueFilter');
	if (leagueFilter) {
		leagueFilter.addEventListener('change', function() {
			const selectedLeague = this.value;
			const matchCards = document.querySelectorAll('.match-card');
			
			matchCards.forEach(card => {
				const league = card.dataset.league;
				if (selectedLeague === 'all' || league === selectedLeague) {
					card.style.display = 'block';
				} else {
					card.style.display = 'none';
				}
			});
		});
	}
	
	// 골 상세 정보 토글
	const goalToggles = document.querySelectorAll('.toggle-goals');
	if (goalToggles.length > 0) {
		goalToggles.forEach(toggle => {
			toggle.addEventListener('click', function(e) {
				e.preventDefault();
				const goalSection = document.getElementById(this.dataset.target);
				if (goalSection) {
					if (goalSection.style.display === 'none') {
						goalSection.style.display = 'block';
						this.innerHTML = 'Hide Goals';
					} else {
						goalSection.style.display = 'none';
						this.innerHTML = 'Show Goals';
					}
				}
			});
		});
	}
	
	// 최근 검색어 저장 및 표시
	const questionInput = document.getElementById('questionInput');
	const recentQuestions = document.getElementById('recentQuestions');
	
	if (questionInput && recentQuestions) {
		// 로컬 스토리지에서 최근 질문 불러오기
		let recentQs = JSON.parse(localStorage.getItem('recentQuestions')) || [];
		
		// 최근 질문 표시
		updateRecentQuestions();
		
		questionForm.addEventListener('submit', function() {
			const question = questionInput.value.trim();
			if (question && !recentQs.includes(question)) {
				recentQs.unshift(question);
				recentQs = recentQs.slice(0, 5); // 최대 5개 저장
				localStorage.setItem('recentQuestions', JSON.stringify(recentQs));
			}
		});
		
		function updateRecentQuestions() {
			if (recentQs.length === 0) {
				recentQuestions.innerHTML = '<em>No recent questions</em>';
				return;
			}
			
			const list = document.createElement('ul');
			list.className = 'list-group';
			
			recentQs.forEach(q => {
				const item = document.createElement('li');
				item.className = 'list-group-item list-group-item-action';
				item.textContent = q;
				item.style.cursor = 'pointer';
				
				item.addEventListener('click', () => {
					questionInput.value = q;
				});
				
				list.appendChild(item);
			});
			
			recentQuestions.innerHTML = '';
			recentQuestions.appendChild(list);
		}
	}
});