from rich.table import Table
from rich.text import Text

def create_league_summary(leagues, console):
	"""
	리그별 경기 요약 테이블 생성
	
	Args:
		leagues (list): 리그 정보 목록
		console (Console): Rich 콘솔 객체
		
	Returns:
		Table: 리그별 경기 수를 보여주는 Rich Table 객체
	"""
	table = Table(title="Football Leagues", show_lines=False)
	
	table.add_column("League", style="cyan")
	table.add_column("Matches", style="green", justify="right")
	
	for league in sorted(leagues, key=lambda x: x["match_count"], reverse=True):
		table.add_row(league["name"], str(league["match_count"]))
	
	return table

def create_goals_summary(matches, console):
	"""
	골 통계 요약 생성
	
	Args:
		matches (list): 경기 목록
		console (Console): Rich 콘솔 객체
		
	Returns:
		Text: 골 통계 텍스트
	"""
	total_goals = 0
	scorers = {}
	
	for match in matches:
		home_score = match.get("home_score", 0)
		away_score = match.get("away_score", 0)
		total_goals += (home_score + away_score)
		
		for goal in match.get("goals", []):
			player = goal.get("player")
			if player:
				scorers[player] = scorers.get(player, 0) + 1
	
	# 최다 득점자 정렬
	top_scorers = sorted(scorers.items(), key=lambda x: x[1], reverse=True)[:5]
	
	summary = Text()
	summary.append(f"Total Goals: ", style="bold")
	summary.append(f"{total_goals}\n\n", style="green")
	
	if top_scorers:
		summary.append("Top Scorers:\n", style="bold")
		for player, goals in top_scorers:
			summary.append(f"• {player}: ", style="cyan")
			summary.append(f"{goals} goal{'s' if goals > 1 else ''}\n", style="green")
	
	return summary