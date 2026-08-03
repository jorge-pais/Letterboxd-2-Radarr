import os
import tomllib
import logging
from dataclasses import dataclass, fields
from pathlib import Path

CONFIG_DIR = Path(os.environ.get("L2R_CONFIG_DIR", os.path.expanduser("~/.config/letterboxd2radarr")))
CONFIG_FILE = CONFIG_DIR / "config.toml"

logger = logging.getLogger("letterboxd2radarr")

@dataclass
class Config:
    @dataclass
    class Radarr:
        api_key : str = ""
        addr : str = "http://localhost"
        port : int = 7878
        profile : str = "HD-1080p"

    @dataclass
    class Flaresolverr:
        addr : str = "http://localhost"
        port : int = 8191

    @dataclass
    class Letterboxd:
        base_url : str = "https://letterboxd.com"

    radarr: Radarr
    flaresolverr: Flaresolverr
    letterboxd: Letterboxd 

    @classmethod
    def load(self, **overrides: dict) -> Config:
        data : dict[str, dict] = {}
        
        if CONFIG_FILE.exists():
            try:
                data = tomllib.loads(CONFIG_FILE.read_text())
            except:
                logger.error("Unable to load config, using default values")
                pass

        def make(section_cls, section_name):
            section_data = data.get(section_name, {})
            section_data.update(overrides.get(section_name, {}))
            # Filter to only valid field names for this dataclass
            valid = { f.name for f in section_cls.__dataclass_fields__.values() }
            return section_cls( **{k: v for k, v in section_data.items() if k in valid} )

        return self(
            radarr=make(self.Radarr, "radarr"),
            flaresolverr=make(self.Flaresolverr, "flaresolverr"),
            letterboxd=make(self.Letterboxd, "letterboxd"),
        )

