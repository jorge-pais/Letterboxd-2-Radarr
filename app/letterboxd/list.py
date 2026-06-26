import logging

from .movie import Movie
from .parser import getMoviesFromLetterboxdWatchlist, getNumberOfPagesFromLetterboxd
from ..flaresolverr import sendGetRequest # how do I solve this

logger = logging.getLogger("letterboxd2radarr")

LETTERBOXD_BASE_URL = "https://letterboxd.com"

def requestWatchlist(user: str):
    url = f"{LETTERBOXD_BASE_URL}/{user}/watchlist"
    
    logger.info(f"Sending request for watchlist page")
    watchlist_page = sendGetRequest(url)
    if not watchlist_page:
        return []

    logger.debug(f"Webpage \n {watchlist_page}")

    movies = getMoviesFromLetterboxdWatchlist(watchlist_page)
    pages = getNumberOfPagesFromLetterboxd(watchlist_page)
    
    if pages > 1:
        for page in range(2, pages + 1):
            logger.info(f"Sending request for watchlist page {page}")
            url = f"{LETTERBOXD_BASE_URL}/{user}/watchlist/page/{page}"
            watchlist_page = sendGetRequest(url)
            if not watchlist_page:
                break

            movies = movies + getMoviesFromLetterboxdWatchlist(watchlist_page)

    return movies

