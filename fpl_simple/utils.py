import ssl
import certifi
import asyncio
import aiohttp

headers = {"User-Agent": ""}
ssl_context = ssl.create_default_context(cafile=certifi.where())

async def fetch(session:aiohttp.ClientSession, url:str, retries:int=5, cooldown=2):
    """Fetches data from the fpl api if needed. This fetch function was inspired from 
    -> https://github.com/amosbastian/fpl/blob/master/fpl/utils.py
    """
    retry_count = 0
    while True:
        try: 
            async with session.get(url, headers=headers, ssl=ssl_context) as response:
                data = await response.json()
                return data
        except aiohttp.client_exceptions.ContentTypeError:
            retry_count += 1

            if retry_count > retries:
                raise Exception(f"Max {retries} exceeded. {url} could not be fetched")
            
            if cooldown:
                await asyncio.sleep(cooldown)

def teamid_converter(team_id: int) -> str:
    teams = {
        1: 'Arsenal', 
        2: 'Aston Villa', 
        3: 'Bournemouth', 
        4: 'Brentford', 
        5: 'Brighton', 
        6: 'Chelsea', 
        7: 'Crystal Palace', 
        8: 'Everton', 
        9: 'Fulham', 
        10: 'Leicester', 
        11: 'Leeds', 
        12: 'Liverpool', 
        13: 'Man City', 
        14: 'Man Utd', 
        15: 'Newcastle', 
        16: "Nott'm Forest", 
        17: 'Southampton', 
        18: 'Spurs', 
        19: 'West Ham', 
        20: 'Wolves'
        }
    return teams[team_id]