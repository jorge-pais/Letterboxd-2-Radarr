import requests
import json

from letterboxd.parser import getMoviesFromLetterboxdList

LETTERBOXD_BASE_URL = "https://letterboxd.com"
LETTERBOXD_USER = "jorg3"
LETTERBOXD_LIST = "watchlist"
TARGET_URL = f"{LETTERBOXD_BASE_URL}/{LETTERBOXD_USER}/{LETTERBOXD_LIST}/page/1"

FLARESOLVERR_PORT = 8191
FLARESOLVERR_ADDR = "127.0.0.1"

try:
    url = f"http://{FLARESOLVERR_ADDR}:{FLARESOLVERR_PORT}/v1"
    headers = {"Content-Type": "application/json"}
    data = {
        "cmd": "request.get",
        "url": TARGET_URL,
        "maxTimeout": 60000
    }
    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        # keys are 'status', 'message', 'solution', 'startTimestamp', 'endTimestamp' and 'version'
        data = response.json()        
        
        page = data['solution']['response']

        print(getMoviesFromLetterboxdList(page))

except requests.exceptions.RequestException as exp:
    print(f"An error as occured: {exp}")
    pass
