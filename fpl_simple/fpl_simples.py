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
from utils import headers, ssl_context


class FPLSIMPLES:
	def __init__(self, session:aiohttp.ClientSession):
		self.session = session
		
		resp = urlopen(URLS["static"], context=ssl_context)
		static = json.loads(resp.read().decode("utf-8"))

		for y, z in static.items():
			setattr(self, y, z)
		
	async def current_pl_teams(self) -> dict:
		"""Returns a list of current teams who are in the Premier league that season"""
		teams = getattr(self, "teams")
		return TEAMS().get_teams(teams)
	
	async def get_team_fixtures(self, team_id:int, next_fixtures:int = 5) -> list:
		"""Returns the Next 5 fixtures of a team based. Minimum number of fixtures is and use assert to check if max not exceeded""" 
		assert next_fixtures < 5, "Error, minimum allowed is 5 fixtures"

		teams = getattr(self, "teams")
		
		team_name = TEAMS().get_teams()[team_id]

		return FIXTURES().next_fixtures()
			

async def main():
	async with aiohttp.ClientSession() as session:
		fpl = FPLSIMPLES(session)
		teams = await fpl.current_pl_teams()
		print(teams)

asyncio.run(main())