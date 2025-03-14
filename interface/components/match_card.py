from rich.panel import Panel
from rich.text import Text
from rich.table import Table

def create_match_card(match, console):
	"""
	경기 결과를 표시하는 카드 형태의 컴포넌트 생성
	
	Args:
		match (dict): 경기 데이터
		console (Console): Rich 콘솔 객체
		
	Returns:
		Panel: 경기 정보를 담은 Rich Panel 객체
	"""
	# 팀 이름과 점수 설정
	home_team = match["home_team"]
	away_team = match["away_team"]
	home_score = match["home_score"]
	away_score = match["away_score"]
	
	# 승자 색상 표시
	home_style = "bold green" if home_score > away_score else "white"
	away_style = "bold green" if away_score > home_score else "white"
	
	if home_score == away_score:
		home_style = away_style = "yellow"
	
	# 제목 구성
	title = Text()
	title.append(f"{match['league']} ", style="blue")
	title.append(f"({match['date']})")
	
	# 경기 정보 테이블
	match_table = Table(show_header=False, box=None)
	match_table.add_column("Team", style="cyan")
	match_table.add_column("Score", justify="center", style="bold")
	
	# 팀 정보 추가
	match_table.add_row(Text(home_team, style=home_style), f"{home_score}")
	match_table.add_row(Text(away_team, style=away_style), f"{away_score}")
	
	# 골 정보가 있으면 추가
	content = [match_table]
	
	if match.get("goals") and len(match["goals"]) > 0:
		goals_text = Text("\nGoals:\n", style="italic")
		
		for goal in match["goals"]:
			scorer = goal["player"]
			team = goal["team"]
			minute = goal["minute"]
			goals_text.append(f"⚽ {minute}' {scorer} ({team})\n")
		
		content.append(goals_text)
	
	return Panel(
		"\n".join(str(item) for item in content),
		title=title,
		border_style="green" if len(match.get("goals", [])) > 0 else "blue"
	)