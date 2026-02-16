from bs4 import BeautifulSoup
import logging

from letterboxd.movie import Movie

logger = logging.getLogger("letterboxd2radarr")

LETTERBOXD_BASE_URL = "https://letterboxd.com"

def getMoviesFromLetterboxdWatchlist(list_html: str):
    # i don't know if it is a good idea to have this initialized everywhere
    soup = BeautifulSoup(list_html, 'html.parser')

    items = soup.find_all('li', class_='griditem') # use this for the watchlist (want to watch and watched)
    # items = soup.find_all('li', class_='posteritem') # use this for regular lists

    films = []
    for item in items:
        poster = item.find('div', class_='react-component')
        if poster:
            film_name = poster.get('data-item-full-display-name', '')
            film_id = poster.get('data-film-id', '')
            film_rel_url = poster.get('data-item-link', '')

            movie = Movie(
                name = film_name, 
                id = film_id, 
                url = f"{LETTERBOXD_BASE_URL}{film_rel_url}")
            films.append(movie)

    if not films:
        logger.warning(f"No movies were able to be scrapped from list")

    return films

# used for when a list has more than a single page
def getNumberOfPagesFromLetterboxd(list_html: str):
    soup = BeautifulSoup(list_html, 'html.parser')

    items = soup.find_all('li', class_='paginate-page')

    last = 1
    for item in items:
        link = item.find('a')
        if link:
            last = link.getText()
        
    return int(last)

