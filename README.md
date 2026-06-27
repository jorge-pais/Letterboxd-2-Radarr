# Letterboxd 2 radarr

This project is presented as an alternative to [letterboxd-list-radarr](https://github.com/screeny05/letterboxd-list-radarr), as that project [may soon be unmaintained](https://github.com/screeny05/letterboxd-list-radarr/issues/64). I believe this is due to letterboxd is now using cloudflare in order to stop scrappers on their website.

I am of course in favour that most bots, nowadays should piss off the internet. It would make sense for letterboxd to be more liberal with their API and the keys they give out. As of right now, their API terms make it clear that no personal project shall use this interface.

## Motivation and goals

This project implements a simple webscrapper for letterboxd, being that all the requests are processed through flaresolverr in order to avoid 403 forbidden from the website. Unlike letterboxd-list-radarr, which exposes a webserver for radarr to connect to thourgh the import lists feature, I want this to be more like a cli tool that I can launch and have this sync automatically (like in a cron job within my arr stack).

Perhaps in the future I'll try and follow that server approach, as it seems simpler to configure. There seems to be a lack of documentation on how [custom lists](https://wiki.servarr.com/radarr/supported#radarrlistimport) work on radarr, and I didn't want to go read the typescript source code for the other project. Also I don't want to use the [letterboxdpy](https://pypi.org/project/letterboxdpy/) package (which would probably save me the trouble of using flaresolverr and writting my own bespoke scraper)

## Features

- [x] Request letterboxd through flaresolverr
    - [Watchlists](https://letterboxd.com/jorg3/watchlist/)
    - [Regular lists](https://letterboxd.com/screeny05/list/jackie-chan-the-definitive-list/)
- [x] Search and add movies to radarr
- [x] Command line interface
    - [ ] Search and add movies from watchlist
    - [ ] do the same from regular lists (and things like directors e.t.c)
- [ ] Configuration file for reading api keys and endpoints
    - [ ] Pass the same parameters via env variables for example
    - [ ] Override parameters via command line options (should be easy using typer)
- [ ] Use database to keep track of sync status between the two
- [ ] Web server for radarr import list support (?)
    - I think this isn't a really important feature

## Development log

### 16-02-2026

The first prototype works already, but matching for name + year is not ideal. Most movies are matched correctly.

But for example, Fly me to the moon (2024) has two entries on radarr, and due to the bug, the second less popular entry was added. This could have been avoided by using TMDB.

Also for some reason, the documentary [_Frogs and How They Live_](https://letterboxd.com/film/frogs-and-how-they-live/), which I am very happy to add to my radarr list. These issues seemed to be solved by adding the first movie that matched with the query. This still has some issues as the name for each film may be different (for e.g. the title on radarr being translated, and thus differing from letterboxd). Also there are movies where the year is incorrect, most times due to the regional releases.

### 26-06-2026 Flaresolverr spamming ?

I think it takes a really long time for flaresolverr to process all the requests, because as of version 0.1.0, I think flaresolverr is creating a session for each individual request. As we have to complete cloudflare's challenge each time, it should really slow us down.

> Analysis: each watchlist request is taking about 11 sec to complete. This totals to 1min53sec for a ~250 movie watchlist of 10 pages
>
> *Solution*: Use flaresolverr sessions in order to preserve cloudflare cookies. First request still takes about 11sec, but subsequent requests will take about 800-1000ms. Total time (with the radarr request which were not accounted for in the previous measurement): 32.3 sec

### Wrong dates

So I've noticed that letterboxd has wrong dates on their pages. For example, Catarina Vasconcelos' The Metamophosis of Birds, shows up as released in 2020, meanwhile in TMDB (which I think is the main source for radarr search) it shows up as released in 2021. This is an issue as we're searching using `'{name} ({year})'` which should yield wrong results.

To solve this I think I'll use a sqlite database. First syncing what movies I have on letterboxd watchlist (each list should be it's own table), and then cross referencing with radarr.

## Running

To run the main program I recommend using `uv`:

```bash
uv run letterboxd-2-radarr watchlist jorg3
uv run letterboxd-2-radarr watchlist jorg3 --dry-run
```

This should create a virtual environement and pull all the necessary dependencies in one go (i think).

Then in order to run flaresolverr, you need the container image from running on a endpoint accessible from your host. You may run the container using the following:

```bash
podman run -d \
  --name=flaresolverr \
  -p 8191:8191 \
  -e LOG_LEVEL=info \
  --restart unless-stopped \
  ghcr.io/flaresolverr/flaresolverr:latest
```
