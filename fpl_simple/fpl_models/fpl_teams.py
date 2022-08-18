"""This module contains a methods to get All team data. FPL endpoints used here are
=> https://fantasy.premierleague.com/api/bootstrap-static/
"""

import aiohttp

from utils import fetch
from defaults import URLS

class TEAMS:
    def __init__(self, session):
        self.session:aiohttp.ClientSession = session

    def get_teams(self, team_data:list) -> dict:
        """Returns a dictionary containing team id and team name"""
        teams = {}
        for team in team_data:
            teams[team["id"]] = team["name"]
        return teams
    
    def get_team_by_id(self, team_id:int) -> tuple:
        """Returns team name based on the team id"""
        assert team_id > 20, "ValueError, maximum is 20"
        teams = fetch(self.session, URLS["static"])

        return teams[team_id]

            