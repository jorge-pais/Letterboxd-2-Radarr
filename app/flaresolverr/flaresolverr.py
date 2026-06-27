import logging
import requests

logger = logging.getLogger("letterboxd2radarr")

FLARESOLVERR_ADDR = "http://127.0.0.1:8191"
DEFAULT_TIMEOUT = 60000 # ms

class FlaresolverrException(Exception):
    pass

class Flaresolverr:
    """This is responsible for a single flaresolverr session"""

    session_id : str = ""
    flareUrl = f""

    def __init__(self, addr = "http://127.0.0.1", port = 8191):
        self.flareUrl = f"{addr}:{port}/v1"

        self._create_session()

        if not self.session_id:
            raise FlaresolverrException("Could not create session for flaresolverr")

    def __del__(self):
        self._destroy_session()

    def request_url(self, url: str) -> str:
        data = {
            "cmd": "request.get",
            "url": url,
            "maxTimeout": DEFAULT_TIMEOUT,
            "session": self.session_id
        }

        response = self._send_request(data)
        if not response:
            logger.error(f"Could not request url: {url}")
            return ""

        page = response['solution']['response']

        request_time = int(response['endTimestamp']) - int(response['startTimestamp'])
        logger.info(f"Request took about {request_time}ms")

        return page

    def _create_session(self):
        data = {
            "cmd": "sessions.create",
            "maxTimeout": 60000
        }

        response = self._send_request(data)
        if not response:
            logger.error("Could not create session")
            return

        self.session_id = response['session']

    def _destroy_session(self):
        if not self.session_id:
            logger.warning("No session was initialized for this flaresolverr object")
            return

        data = {
            "cmd": "sessions.destroy",
            "maxTimeout": 60000,
            "session": self.session_id
        }

        response = self._send_request(data)
        if not response:
            logger.error("Something went wrong destroying the session")
        
    def _send_request(self, data):
        headers = {"Content-Type": "application/json"}
        try: 
            response = requests.post(self.flareUrl, headers=headers, json=data)
            code = response.status_code

            if code != 200:
                logger.error(f"Unexpected status code: {code}") 
                return None

            result = response.json()
            return result

        except Exception as e:
            logger.error(f"Exception was thrown: {e}")
            pass

        return None

