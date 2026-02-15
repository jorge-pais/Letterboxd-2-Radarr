# Letterboxd 2 radarr

This project is presented as an alternative to [letterboxd-list-radarr](https://github.com/screeny05/letterboxd-list-radarr), as that project [may soon be unmaintained](https://github.com/screeny05/letterboxd-list-radarr/issues/64). I believe this is due to letterboxd is now using cloudflare in order to stop scrappers on their website.

I am of course in favour that most bots now, should piss off the net, but also it would make sense for letterboxd to be more liberal with their API endpoints and the keys they give out. As right now their API terms make it clear that no personal project shall use this API.

## Features

- [ ] Request letterboxd through flaresolverr
    - [Watchlists](https://letterboxd.com/jorg3/watchlist/)
    - [Regular lists](https://letterboxd.com/screeny05/list/jackie-chan-the-definitive-list/)
    - [Watched movies](https://letterboxd.com/jorg3/films/)
    - Filmography such as:
        - [Actor](https://letterboxd.com/actor/tom-hanks/)
        - [Director](https://letterboxd.com/director/alfred-hitchcock/)
        - [Writer](https://letterboxd.com/writer/charlie-kaufman/)
    - [Collections](https://letterboxd.com/films/in/halloween-collection/)
    - [Popular movies](https://letterboxd.com/films/popular/)
- [ ] Add movies to radarr 
- [ ] Use database to keep track of sync status between the two
- [ ] Rust rewrite?

## Running flaresolverr

```
docker run -d \
# podman run -d \
  --name=flaresolverr \
  -p 8191:8191 \
  -e LOG_LEVEL=info \
  --restart unless-stopped \
  ghcr.io/flaresolverr/flaresolverr:latest
```
