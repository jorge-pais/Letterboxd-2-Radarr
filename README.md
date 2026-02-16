# Letterboxd 2 radarr

This project is presented as an alternative to [letterboxd-list-radarr](https://github.com/screeny05/letterboxd-list-radarr), as that project [may soon be unmaintained](https://github.com/screeny05/letterboxd-list-radarr/issues/64). I believe this is due to letterboxd is now using cloudflare in order to stop scrappers on their website.

I am of course in favour that most bots, nowadays should piss off the internet. It would make sense for letterboxd to be more liberal with their API and the keys they give out. As of right now, their API terms make it clear that no personal project shall use this interface.

## Motivation and goals

This project implements a simple webscrapper for letterboxd, being that all the requests are processed through flaresolverr in order to avoid 403 forbidden from the website. Unlike letterboxd-list-radarr, which exposes a webserver for radarr to connect to thourgh the import lists feature, I want this to be more like a cli tool that I can launch and have this sync automatically (like in a cron job within my arr stack).

Perhaps in the future I'll try and follow that server approach, as it seems simpler to configure. There seems to be a lack of documentation on how [custom lists](https://wiki.servarr.com/radarr/supported#radarrlistimport) work on radarr, and I didn't want to go read the typescript source code for the other project.  

## Features

- [x] Request letterboxd through flaresolverr
    - [Watchlists](https://letterboxd.com/jorg3/watchlist/)
    - [Regular lists](https://letterboxd.com/screeny05/list/jackie-chan-the-definitive-list/)
- [x] Search and add movies to radarr
- [x] Command line interface
- [ ] Configuration file for reading api keys and endpoints
- [ ] Use database to keep track of sync status between the two
- [ ] Docker image (?)
- [ ] Web server for radarr import list support (?)

## Development log

The first prototype works already, but matching for name + year is not ideal. Most movies are matched correctly.

But for example, Fly me to the moon (2024) has two entries on radarr, and due to the bug, the second less popular entry was added. This could have been avoided by using TMDB.

Also for some reason, the documentary [_Frogs and How They Live_](https://letterboxd.com/film/frogs-and-how-they-live/), which I am very happy to add to my radarr list. These issues seemed to be solved by adding the first movie that matched with the query. This still has some issues as the name for each film may be different (for e.g. the title on radarr being translated, and thus differing from letterboxd). Also there are movies where the year is incorrect, most times due to the regional releases.

## Running flaresolverr

```bash
podman run -d \
  --name=flaresolverr \
  -p 8191:8191 \
  -e LOG_LEVEL=info \
  --restart unless-stopped \
  ghcr.io/flaresolverr/flaresolverr:latest
```
