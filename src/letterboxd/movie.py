from dataclasses import dataclass

@dataclass
class Movie:
    name: str = ""
    id: str = ""
    url: str = ""
    imdb: str = ""
    tmdb: str = ""
