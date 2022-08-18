"""
FPL Simple module

All the endpoints to the Fantansy premier league api are called from here including
getting specified data.
"""

import aiohttp
import json
import asyncio
import certifi

from urllib.request import urlopen

from fpl_models.fpl_fixture import FIXTURES
from fpl_models.fpl_teams import TEAMS
from defaults import URLS
from utils import headers, ssl_context, fetch, teamid_converter


class FPLSIMPLES:
	def __init__(self, session:aiohttp.ClientSession):
		self.session = session
		
		resp = urlopen(URLS["static"], context=ssl_context)
		static = json.loads(resp.read().decode("utf-8"))

		for y, z in static.items():
			setattr(self, y, z)
		
		all_events = static["events"]


		for events in all_events:
			if events["is_current"] == True:
				setattr(self, "current_gameweek", events["id"])
				break
	

	async def current_pl_teams(self) -> dict:
		"""Returns a list of current teams who are in the Premier league that season"""
		teams = getattr(self, "teams")
		return TEAMS(self.session).get_teams(teams)
	

	async def get_team_fixtures(self, team_id:int, next_fixtures:int = 5) -> list:
		"""Returns upcoming fixtures of a team based. Minimum number of fixtures is and use assert to check if max not exceeded""" 
		assert next_fixtures <= 5, "Error, maximum allowed is 5 fixtures"
		assert team_id <= 20, "Error, team_id must be in the range [1-20]"

		# cut gameweek id if it's close to matchday 33
		if getattr(self, "current_gameweek") > 33:
			if getattr(self, "current_gameweek") == 34:
				next_fixtures = 4
			elif getattr(self, "current_gameweek") == 35:
				next_fixtures = 3
			elif getattr(self, "current_gameweek") == 36:
				next_fixtures = 2
			elif getattr(self, "current_gameweek") == 37:
				next_fixtures = 1
			elif getattr(self, "current_gameweek") == 38:
				next_fixtures = 0

		data = await fetch(self.session, URLS["ffixtures"])

		return FIXTURES(data, getattr(self, "current_gameweek")).next_fixtures(team_id, next_fixtures)

	async def get_all_fixtures(self):
		"""Returns a list[str, tuple] containing the all the years fixtures"""
		data = await fetch(self.session, URLS["fixtures"])

		return FIXTURES(data).all_fixtures() 

	async def get_gameweek_fixtures(self, gameweek_id:int):
		"""Returns a List[dict{str, tuple}] containing all fixtures for a particular gameweek"""
		assert gameweek_id <= 38, f"Error, Max number of matchdays is 38 not {gameweek_id}"
		
		data = await fetch(self.session, URLS["fixtures"])

		return FIXTURES(data).gameweek_fixtures(gameweek_id)

			

async def main():
	async with aiohttp.ClientSession() as session:
		fpl = FPLSIMPLES(session)
		teams = await fpl.get_gameweek_fixtures(39)
		print(teams)

asyncio.run(main())