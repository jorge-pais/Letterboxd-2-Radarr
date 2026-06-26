import logging
import sys
import argparse

import typer

from .letterboxd import requestWatchlist
from .radarr import Radarr # todo change this bullshit

parser = argparse.ArgumentParser()

app = typer.Typer(
    add_completion=False,
    no_args_is_help=True
)

logger = logging.getLogger("letterboxd2radarr")
file_handler = logging.FileHandler(filename='tmp.log')
stdout_handler = logging.StreamHandler(stream=sys.stdout)

@app.command()
def watchlist(
    user: str = typer.Argument(None, 
        help="User name to scrape"), 
    dry_run: bool = typer.Option(False, "--dry-run", 
        help="Scrapes letterboxd and won't add anything to radarr")
) -> None:
    """Scrape a user's watchlist from letterboxd and import it into radarr"""

    logging.basicConfig(
        level = logging.INFO,
        handlers = [file_handler, stdout_handler],
        format='[%(asctime)s] %(name)s {%(filename)s:%(lineno)d} %(levelname)s - %(message)s',
    )
    logger.info("Starting up")

    radarr = Radarr(dry_run = dry_run)

    logger.info(f"Requesting watchlist for user {user}")
    movies = requestWatchlist(user)

    if not len(movies):
        logger.error("No movies found in that watchlist")
        exit(1)

    logger.info("Adding movies to radarr now")
    for movie in movies:
        logger.info(f"Searching for {movie.name}")
        radarr.searchMovieAndAdd(movie.name)

@app.command()
def list(url: str):
    """*not implemented yet*"""
    pass

def main() -> None:
    app()

if __name__ == '__main__':
    main()
