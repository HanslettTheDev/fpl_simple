import aiohttp
import json
import asyncio
import requests



ness = json.load(open("bootstrap-static.json"))
print(ness["total_players"])
# async def get_player_names():
#   async with aiohttp.ClientSession() as session:
#     async with session.get("https://fantasy.premierleague.com/api/bootstrap-static/") as response:
#       data = await response.read()
#       print(data)

# asyncio.run(get_player_names())



