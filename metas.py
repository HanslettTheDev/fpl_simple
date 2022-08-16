import aiohttp
import json
import asyncio

import certifi
import ssl

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

headers = {"User-Agent": ""}
ssl_context = ssl.create_default_context(cafile=certifi.where())

async def get_player_names():
  async with aiohttp.ClientSession() as session:
    async with session.get(url="https://fantasy.premierleague.com/api/bootstrap-static/", headers=headers, ssl_context=ssl_context) as response:
      data = await response.json()
  with open("fpl.json", "w") as f:
    json.dump(data, f, indent=4)

def checks():
  with open("fpl.json", "r") as f:
    data = json.load(f)

  print(data["events"][0].keys())

checks()      

# asyncio.run(get_player_names())