from .list import requestWatchlist
from .movie import Movie
from .parser import (
    getMoviesFromLetterboxdWatchlist,
    getNumberOfPagesFromLetterboxd
)

__all__ = [
    "requestWatchlist",
    "Movie",
    "getNumberOfPagesFromLetterboxd",
    "getMoviesFromLetterboxdWatchlist"
]
