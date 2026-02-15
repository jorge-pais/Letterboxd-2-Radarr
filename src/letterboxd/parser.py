from bs4 import BeautifulSoup

def getMoviesFromLetterboxdList(list_html: str):
    soup = BeautifulSoup(list_html, 'html.parser')

    items = soup.find_all('li', class_='griditem')

    films = []

    for item in items:
        poster = item.find('div', class_='react-component')
        if poster:
            film_name = poster.get('data-item-full-display-name', '')
            film_id = poster.get('data-film-id', '')
            film_rel_url = poster.get('data-item-link', '')

            films.append({
                'name': film_name,
                'id': film_id,
                'url': film_rel_url
            })

    return films

