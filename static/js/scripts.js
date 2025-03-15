// Football Matches Q&A Bot client script
document.addEventListener('DOMContentLoaded', function() {
	// Show loading indicator on form submit
	const questionForm = document.getElementById('questionForm');
	if (questionForm) {
		questionForm.addEventListener('submit', function(e) {
			e.preventDefault();
			const submitBtn = this.querySelector('button[type="submit"]');
			const originalText = submitBtn.innerHTML;
			
			submitBtn.innerHTML = `
				<div class="loader">
					<span class="loader-dot"></span>
					<span class="loader-dot"></span>
					<span class="loader-dot"></span>
				</div>
			`;
			submitBtn.disabled = true;
			
			 // Add actual question request handling code here
			// Currently using setTimeout for demo purposes
			const question = document.getElementById('questionInput').value;
			
			setTimeout(() => {
				// Placeholder for API call and response handling
				displayAnswer(`Generating answer for "${question}". When the actual API is connected, the answer will appear here.`);
				submitBtn.innerHTML = originalText;
				submitBtn.disabled = false;
			}, 1500);
		});
	}
	
	// Match filtering
	const leagueFilter = document.getElementById('leagueFilter');
	if (leagueFilter) {
		leagueFilter.addEventListener('change', function() {
			const selectedLeague = this.value;
			const matchCards = document.querySelectorAll('.match-card');
			
			matchCards.forEach(card => {
				const league = card.dataset.league;
				if (selectedLeague === 'all' || league === selectedLeague) {
					card.style.display = 'block';
					setTimeout(() => {
						card.style.opacity = '1';
						card.style.transform = 'translateY(0)';
					}, 10);
				} else {
					card.style.opacity = '0';
					card.style.transform = 'translateY(20px)';
					setTimeout(() => {
						card.style.display = 'none';
					}, 300);
				}
			});
		});
	}
	
	// Toggle goal details
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
	
	// Save and display recent questions
	const questionInput = document.getElementById('questionInput');
	const recentQuestions = document.getElementById('recentQuestions');
	
	if (questionInput && recentQuestions) {
		// Load recent questions from local storage
		let recentQs = JSON.parse(localStorage.getItem('recentQuestions')) || [];
		
		// Display recent questions
		updateRecentQuestions();
		
		questionForm.addEventListener('submit', function() {
			const question = questionInput.value.trim();
			if (question && !recentQs.includes(question)) {
				recentQs.unshift(question);
				recentQs = recentQs.slice(0, 5); // Store up to 5 questions
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

		function clearRecentQuestions() {
			localStorage.removeItem('recentQuestions');
			updateRecentQuestions();
		}

		// Add a button to clear recent questions
		const clearBtn = document.createElement('button');
		clearBtn.textContent = 'Clear Recent Questions';
		clearBtn.className = 'btn btn-danger';
		clearBtn.addEventListener('click', clearRecentQuestions);
		document.querySelector('.input-area')?.appendChild(clearBtn);
	}

	// Add animation effects
	const animateElements = () => {
		const elements = document.querySelectorAll('.animate__animated:not(.animate__fadeInUp)');
		elements.forEach(element => {
			if (isElementInViewport(element)) {
				element.classList.add('animate__fadeInUp');
			}
		});
	}

	// Connect animation to scroll events
	window.addEventListener('scroll', animateElements);
	
	// Match card dynamic creation function
	window.createMatchCard = (match) => {
		const card = document.createElement('div');
		card.className = 'match-card animate__animated animate__fadeIn';
		card.dataset.league = match.league;
		
		let winnerClass = '';
		if (match.home_score > match.away_score) {
			winnerClass = 'winner-home';
		} else if (match.away_score > match.home_score) {
			winnerClass = 'winner-away';
		} else {
			winnerClass = 'match-draw';
		}
		
		let goalsHTML = '';
		if (match.goals && match.goals.length > 0) {
			goalsHTML = `
				<div class="goal-details">
					<h4>Goal Scorers</h4>
					<ul class="goal-list">
						${match.goals.map(goal => 
							`<li class="goal-item">
								<span class="goal-minute">${goal.minute}'</span> 
								${goal.player} (${goal.team})
							</li>`
						).join('')}
					</ul>
				</div>
			`;
		}
		
		card.innerHTML = `
			<div class="match-card-header">
				<span class="league-badge">${match.league}</span>
				<small>${match.date}</small>
			</div>
			<div class="match-card-content">
				<div class="match-teams ${winnerClass}">
					<div class="team-home">
						<div class="team-name">${match.home_team}</div>
					</div>
					<div class="score">${match.home_score} - ${match.away_score}</div>
					<div class="team-away">
						<div class="team-name">${match.away_team}</div>
					</div>
				</div>
				${goalsHTML}
			</div>
		`;
		
		return card;
	}

	// Display match cards using sample data (for demo)
	const displaySampleMatches = () => {
		const sampleMatches = [
			{
				league: "Premier League",
				date: "2023-05-15",
				home_team: "Manchester United",
				away_team: "Liverpool",
				home_score: 2,
				away_score: 1,
				goals: [
					{ minute: 23, player: "Bruno Fernandes", team: "Manchester United" },
					{ minute: 45, player: "Marcus Rashford", team: "Manchester United" },
					{ minute: 78, player: "Mohamed Salah", team: "Liverpool" }
				]
			},
			{
				league: "La Liga",
				date: "2023-05-15",
				home_team: "Barcelona",
				away_team: "Real Madrid",
				home_score: 3,
				away_score: 3,
				goals: [
					{ minute: 12, player: "Robert Lewandowski", team: "Barcelona" },
					{ minute: 25, player: "Vinicius Jr", team: "Real Madrid" },
					{ minute: 34, player: "Pedri", team: "Barcelona" },
					{ minute: 56, player: "Karim Benzema", team: "Real Madrid" },
					{ minute: 67, player: "Raphinha", team: "Barcelona" },
					{ minute: 89, player: "Rodrygo", team: "Real Madrid" }
				]
			},
			{
				league: "Serie A",
				date: "2023-05-15",
				home_team: "AC Milan",
				away_team: "Inter Milan",
				home_score: 0,
				away_score: 2,
				goals: [
					{ minute: 34, player: "Lautaro Martinez", team: "Inter Milan" },
					{ minute: 78, player: "Romelu Lukaku", team: "Inter Milan" }
				]
			}
		];
		const matchCardsContainer = document.getElementById('matchCards');
		if (matchCardsContainer) {
			// Add league filter options
			const leagueFilter = document.getElementById('leagueFilter');
			const leagues = [...new Set(sampleMatches.map(match => match.league))];
			leagues.forEach(league => {
				const option = document.createElement('option');
				option.value = league;
				option.textContent = league;
				leagueFilter.appendChild(option);
			});
			// Add match cards
			sampleMatches.forEach(match => {
				const card = createMatchCard(match);
				matchCardsContainer.appendChild(card);
			});
		}
	}
	// Display sample data (until API is connected)
	displaySampleMatches();
	
	// Display answer with animation
	const displayAnswer = (answer) => {
		const answerSection = document.getElementById('answer');
		if (!answerSection) return;
		
		let demoNotice = '';
		if (window.isDemoMode) {
			demoNotice = `<div class="demo-notice"><p><strong>Note:</strong> This is a demo response. Connect to the API for real answers.</p></div>`;
		}
		
		answerSection.innerHTML = `
			<div class="answer-container animate__animated animate__fadeInUp">
				<h3>Answer</h3>
				${demoNotice}
				<p>${answer}</p>
			</div>
		`;
		
		// Scroll to answer
		answerSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
	}

	// 불필요한 주석과 중복 코드 제거, isElementInViewport 함수 정리
	function isElementInViewport(el) {
		const rect = el.getBoundingClientRect();
		return (
			rect.top >= 0 &&
			rect.left >= 0 &&
			rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
			rect.right <= (window.innerWidth || document.documentElement.clientWidth)
		);
	}

	// API 상태 체크 함수 정리
	function checkApiStatus() {
		fetch('/api/status')
			.then(response => response.json())
			.then(data => {
				const statusIndicator = document.querySelector('.status-indicator');
				const statusText = document.querySelector('.status-text');
				
				if (data.status === 'online') {
					statusIndicator.classList.remove('offline');
					statusIndicator.classList.add('online');
					statusText.textContent = 'API Status: Online (Live Data)';
					window.isDemoMode = false;
				}
			})
			.catch(err => {
				console.log('API status check failed:', err);
			});
	}

	// 초기 애니메이션 실행
	setTimeout(animateElements, 100);

	// API 상태 주기적 체크 (1분)
	setInterval(checkApiStatus, 60000);

	// Enhanced animations for page elements
	function animateElement(el, animation = 'fadeIn', delay = 0) {
		el.style.opacity = '0';
		setTimeout(() => {
			el.style.opacity = '1';
			el.classList.add('animate__animated', `animate__${animation}`);
			el.addEventListener('animationend', () => {
				el.classList.remove('animate__animated', `animate__${animation}`);
			});
		}, delay);
	}

	// Animate goals with delay for staggered effect
	function animateGoalItems() {
		const goalItems = document.querySelectorAll('.goal-item');
		goalItems.forEach((item, index) => {
			item.style.setProperty('--animation-order', index);
		});
	}

	// Add scroll reveal animations
	function setupScrollAnimations() {
		const animatedElements = document.querySelectorAll('.match-card, .answer-container, .question-form');
		
		const observer = new IntersectionObserver((entries) => {
			entries.forEach(entry => {
				if (entry.isIntersecting) {
					entry.target.classList.add('fade-in');
					observer.unobserve(entry.target);
				}
			});
		}, {
			threshold: 0.1,
			rootMargin: '0px 0px -50px 0px'
		});
		
		animatedElements.forEach(el => observer.observe(el));
	}

	// Add parallax effect to match cards
	function setupParallax() {
		const cards = document.querySelectorAll('.match-card');
		
		document.addEventListener('mousemove', event => {
			const { clientX, clientY } = event;
			const centerX = window.innerWidth / 2;
			const centerY = window.innerHeight / 2;
			
			cards.forEach(card => {
				const rect = card.getBoundingClientRect();
				if (isElementInViewport(card)) {
					const cardCenterX = rect.left + rect.width / 2;
					const cardCenterY = rect.top + rect.height / 2;
					
					const offsetX = (clientX - cardCenterX) / 40;
					const offsetY = (clientY - cardCenterY) / 40;
					
					card.style.transform = `translate(${offsetX}px, ${offsetY}px) scale(1.01)`;
				}
			});
		});
		
		// Reset transform when not hovering
		cards.forEach(card => {
			card.addEventListener('mouseleave', () => {
				card.style.transform = '';
			});
		});
	}

	// Add match card flip effect
	function setupCardFlipEffects() {
		const cards = document.querySelectorAll('.match-card');
		
		cards.forEach(card => {
			card.addEventListener('click', () => {
				if (!card.classList.contains('flipping')) {
					card.classList.add('flipping');
					card.style.transform = 'rotateY(180deg)';
					
					setTimeout(() => {
						card.classList.remove('flipping');
						card.style.transform = '';
					}, 1500);
				}
			});
		});
	}

	// Add dynamic background effects
	function setupDynamicBackground() {
		const root = document.documentElement;
		
		document.addEventListener('mousemove', event => {
			const { clientX, clientY } = event;
			const moveX = clientX / window.innerWidth - 0.5;
			const moveY = clientY / window.innerHeight - 0.5;
			
			root.style.setProperty('--bg-position-x', moveX * 10 + 'px');
			root.style.setProperty('--bg-position-y', moveY * 10 + 'px');
		});
	}

	// Add interactive header elements
	function setupHeaderInteractions() {
		const header = document.querySelector('.app-header');
		const title = document.querySelector('.app-title');
		
		window.addEventListener('scroll', () => {
			const scrollPos = window.scrollY;
			// Scale down the header slightly on scroll
			if (scrollPos > 50) {
				header.style.transform = 'scale(0.98)';
				header.style.boxShadow = '0 8px 20px rgba(0,0,0,0.15)';
			} else {
				header.style.transform = 'scale(1)';
				header.style.boxShadow = '0 4px 12px var(--shadow-color)';
			}
		});
		
		title.addEventListener('mouseover', () => {
			title.classList.add('animate__rubberBand');
			setTimeout(() => {
				title.classList.remove('animate__rubberBand');
			}, 1000);
		});
	}

	// Initialize dynamic effects
	setTimeout(() => {
		setupScrollAnimations();
		setupDynamicBackground();
		setupHeaderInteractions();
		animateGoalItems();
	}, 500);
});