import logging
import sys
import argparse

from letterboxd.list import requestWatchlist
from radarr.radarr import Radarr # todo change this bullshit

parser = argparse.ArgumentParser()

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Import your Letterboxd watchlist into Radarr",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --user jorg3
  %(prog)s --user jorg3 --dry-run
  %(prog)s --user jorg3 --config /path/to/config.ini
  %(prog)s --help
        """
    )
    
    parser.add_argument(
        '--user', 
        '-u',
        type=str,
        required=True,
        help='Letterboxd username to import watchlist from'
    )
    
    parser.add_argument(
        '--dry_run', 
        '-d',
        action='store_true',
        help='Perform a dry run without actually adding movies to Radarr'
    )
    
    return parser.parse_args()

logger = logging.getLogger("letterboxd2radarr")
file_handler = logging.FileHandler(filename='tmp.log')
stdout_handler = logging.StreamHandler(stream=sys.stdout)

def main():
    args = parse_arguments()

    logging.basicConfig(
        level = logging.INFO,
        handlers = [file_handler, stdout_handler],
        format='[%(asctime)s] %(name)s {%(filename)s:%(lineno)d} %(levelname)s - %(message)s',
    )
    logger.info("Starting up")

    print(args.dry_run)
    
    radarr = Radarr(dry_run = args.dry_run)

    logger.info(f"Requesting watchlist for user {args.user}")
    movies = requestWatchlist(args.user)

    if not len(movies):
        logger.error("No movies found in that watchlist")
        exit(1)

    logger.info("Adding movies to radarr now")
    for movie in movies:
        logger.info(f"Searching for {movie.name}")
        radarr.searchMovieAndAdd(movie.name)

if __name__ == '__main__':
    main()
