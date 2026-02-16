import logging
import requests

logger = logging.getLogger("letterboxd2radarr")

FLARESOLVERR_ADDR = "http://127.0.0.1:8191"

def sendGetRequest(url: str):
    flareUrl = f"{FLARESOLVERR_ADDR}/v1"
    headers = {"Content-Type": "application/json"}
    data = {
        "cmd": "request.get",
        "url": url,
        "maxTimeout": 60000
    }

    try: 
        response = requests.post(flareUrl, headers=headers, json=data)
        code = response.status_code
        if code != 200:
            logger.error(f"Unexpected status code: {code}") 
            return ""

        # keys are 'status', 'message', 'solution', 'startTimestamp', 'endTimestamp' and 'version'
        data = response.json()
        page = data['solution']['response']

        return page
    except Exception as e:
        logger.error(f"Exception was thrown: {e}")
        pass

    return ""
