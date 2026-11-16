import logging

from .parser import getIndividualMovieInfo
from dataclasses import dataclass
from ..flaresolverr import Flaresolverr

logger = logging.getLogger("letterboxd2radarr")

@dataclass
class Movie:
    name: str = ""
    id: str = ""
    url: str = ""
    imdb: str = ""
    tmdb: str = ""

def requestMovie(url: str, flare: Flaresolverr):
    logger.info(f"Sending movie page request")
    
    movie_page = flare.request_url(url)
    if not movie_page:
        logger.error(f"Couldn't request movie page for {url}")
        return None
    
    logger.info(f"Webpage {movie_page}")

    getIndividualMovieInfo(movie_page)
    
