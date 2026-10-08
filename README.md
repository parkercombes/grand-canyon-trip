# Grand Canyon Trip

An interactive map of a four-day road trip, Oct 4–7, 2026. It starts and ends in Las Vegas and covers Valley of Fire, the Grand Canyon North Rim, Coral Pink Sand Dunes, Four Corners, Monument Valley and Upper Antelope Canyon.

**Live map:** https://parkercombes.github.io/grand-canyon-trip/

Also published as a Claude artifact: https://claude.ai/artifact/3bULgNb34SAS4Qeo1ETo7V (private; use the page's Share menu to give people access).

## The itinerary

| Day | Date | Route | Night |
|---|---|---|---|
| 1 | Sun Oct 4 | Polo Towers (Las Vegas) → Valley of Fire → Kanab | Hampton Inn Kanab |
| 2 | Mon Oct 5 | North Rim: all of Cape Royal Road, then Point Imperial, then the Visitor Center. Coral Pink Sand Dunes at sunset. | Hampton Inn Kanab |
| 3 | Tue Oct 6 | Four Corners Monument → Kayenta. Monument Valley (The View) for stargazing. | Hampton Inn Kayenta |
| 4 | Wed Oct 7 | Upper Antelope Canyon tour in Page → Las Vegas | Waldorf Astoria Las Vegas |

Zion was closed, so the drives between Las Vegas and Kanab go I‑15 to Hurricane, then Colorado City and Fredonia.

## What's in the repo

| Path | What it is |
|---|---|
| `index.html` | The map page (Leaflet). Route data is inlined in the `TRIP` constant. |
| `tiles/` | USGS basemap tiles (topo and satellite), bundled as base64 JSON by zoom level. The page loads them on demand. |
| `data/trip.json` | Stop coordinates and road routes for each drive. |
| `scripts/routes.py` | Rebuilds `data/trip.json` from the stop list using the public OSRM router. |
| `scripts/tiles.py` | Downloads USGS tiles around the routes and rebuilds `tiles/`. |
| `scripts/inline_trip.py` | Copies `data/trip.json` into `index.html`. |

## View it locally

The page fetches the tile bundles, so serve the folder instead of opening the file directly:

```bash
python3 -m http.server 8765 --bind 127.0.0.1
```

Then open http://127.0.0.1:8765.

## Change a route

1. Edit the stops or their order in `SEG` (and coordinates in `P`) in `scripts/routes.py`.
2. Run `python3 scripts/routes.py`, then `python3 scripts/inline_trip.py`.
3. If the routes now cover new ground, run `python3 scripts/tiles.py` to fetch the extra basemap tiles.
4. Update the stop lists, dates and notes in the `DAYS` and `PLACES` constants in `index.html` to match.

Routes are the most likely roads between stops, not GPS tracks. Mileage and drive times don't include stops or traffic.

## Credits

Basemap: USGS The National Map (public domain). Routing: OSRM with OpenStreetMap data. Map library: Leaflet.
