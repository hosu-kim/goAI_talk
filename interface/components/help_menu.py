from rich.panel import Panel
from rich.markdown import Markdown

def create_help_menu(console):
	"""
	도움말 메뉴 생성
	
	Args:
		console (Console): Rich 콘솔 객체
		
	Returns:
		Panel: 도움말 정보를 담은 Rich Panel
	"""
	help_text = """
	# Football Q&A Bot - Help Menu

	## Available Commands

	* `help` - Show this help message
	* `exit`, `quit`, `q` - Exit the application
	* `refresh`, `update` - Refresh match data from API
	* `leagues`, `competitions` - Show available leagues
	* `teams` - Show available teams
	* `matches` - Show summary of yesterday's matches
	* `stats` - Show match statistics

	## Example Questions

	* "Who won the Premier League match yesterday?"
	* "Did Manchester United play yesterday?"
	* "How many goals were scored in La Liga?"
	* "Who scored for Arsenal?"
	* "Which team had the most goals yesterday?"
	* "Show me the results from Serie A"
	"""
	
	md = Markdown(help_text)
	return Panel(md, title="Help", border_style="blue", width=80)