import logging

from arrapi import RadarrAPI, Movie, QualityProfile, RootFolder

logger = logging.getLogger("letterboxd2radarr")

RADARR_API_KEY = ""
RADARR_ADDR = "http://localhost:7878"
TARGET_PROFILE = "HD-1080p"

class Radarr:
    radarr : RadarrAPI
    quality_profile : QualityProfile
    root_folder : RootFolder
    dry_run : bool

    def __init__(self, dry_run = False):
        self.radarr = RadarrAPI(RADARR_ADDR, RADARR_API_KEY)
        self.quality_profile = [p for p in self.radarr.quality_profile() if p.name == TARGET_PROFILE][0]
        self.root_folder = self.radarr.root_folder()[0]
        self.dry_run = dry_run

    def searchMovieAndAdd(self, title: str, begin_search: bool = False):
        results = self.radarr.search_movies(title)

        found_movie = None
        for movie in results:
            full_title = f"{movie.title} ({movie.year})"
            if title in full_title:
                logger.info(f"Found name match for {full_title} TMDB: {movie.tmdbId}")
                found_movie = movie
                break

        if not found_movie:
            logger.error(f"Unable to get movie for {title}")
            return False
        
        if not self.dry_run:
            try:
                found_movie.add(
                    root_folder = self.root_folder, 
                    quality_profile = self.quality_profile, 
                    monitor = True, 
                    search = begin_search)
            except Exception as e: 
                logger.warning(f"Caught exception: {e}") 

        return True

