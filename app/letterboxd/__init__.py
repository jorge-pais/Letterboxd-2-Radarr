from .list import requestWatchlist
from .movie import Movie, requestMovie
from .parser import (
    getMoviesFromLetterboxdWatchlist,
    getNumberOfPagesFromLetterboxd,
    getIndividualMovieInfo
)

__all__ = [
    "requestWatchlist",
    "requestMovie",
    "Movie",
    "getNumberOfPagesFromLetterboxd",
    "getMoviesFromLetterboxdWatchlist",
    "getIndividualMovieInfo"
]
