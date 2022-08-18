"""This module contains all the methods to get fixtures from the fantasy premier league api
The information and endpoints used for this particular module are taken from this links
=> https://fantasy.premierleague.com/api/fixtures/
=> https://fantasy.premierleague.com/api/element-summary/%7Belement_id%7D/
"""


from defaults import URLS
from utils import teamid_converter

class FIXTURES:
	def __init__(self, fixture_data:list, current_gameweek:int = 0):
		self.fixture_data = fixture_data
		self.current_gameweek = current_gameweek

	def next_fixtures(self, team_id: int, next_fixtures:int) -> list:
		"""Returns the fixtures for a specific team both away and home games"""
		all_fixtures = [{fixture["event"]: (fixture["team_h"], fixture["team_a"])} for fixture in self.fixture_data if fixture["team_h"] == team_id or fixture["team_a"] == team_id]

		team_fixtures = [fixture for i, fixture in zip([i for i in range(next_fixtures)], all_fixtures)]
		
		# convert team fixtures to their team names
		named_fixtures = [{f"Gameweek {str(t)}": f"{teamid_converter(u[0])} vs {teamid_converter(u[1])}"} for tf in team_fixtures for t, u in tf.items()]
		
		return named_fixtures
	
	def all_fixtures(self):
		all_fixtures = [{"Gameweek {}".format(str(fixture["event"])): (teamid_converter(fixture["team_h"]), teamid_converter(fixture["team_a"]))} for fixture in self.fixture_data]
		
		return all_fixtures

	def gameweek_fixtures(self, gameweek_id:int):
		"""Return gameweek fixtures for a particular gameweek"""

		gameweek_fixtures = [{"Gameweek {}".format(str(fixture["event"])): (teamid_converter(fixture["team_h"]), teamid_converter(fixture["team_a"]))} for fixture in self.fixture_data if fixture["event"] == gameweek_id]

		return gameweek_fixtures