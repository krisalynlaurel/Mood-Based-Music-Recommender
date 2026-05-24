import requests
import os
from dotenv import load_dotenv

load_dotenv()

LASTFM_API_KEY = os.getenv("LASTFM_API_KEY")
BASE_URL = "http://ws.audioscrobbler.com/2.0/"


def search_tracks_by_mood(query, limit=10):
    try:
        params = {
            "method": "track.search",
            "track": query,
            "api_key": LASTFM_API_KEY,
            "format": "json",
            "limit": limit
        }
        response = requests.get(BASE_URL, params=params)
        data = response.json()
        items = data.get("results", {}).get("trackmatches", {}).get("track", [])
        tracks = []
        for item in items:
            image_url = None
            for img in item.get("image", []):
                if img.get("size") == "large":
                    image_url = img.get("#text")
            tracks.append({
                "name": item.get("name", "Unknown"),
                "artist": item.get("artist", "Unknown"),
                "album": "Last.fm",
                "url": item.get("url", "#"),
                "preview_url": None,
                "image": image_url,
                "duration_ms": 180000,
                "popularity": int(item.get("listeners", 0)) // 10000,
            })
        return tracks
    except Exception as e:
        print(f"Last.fm API error: {e}")
        return []


def get_mixed_recommendations(mood_label, limit=10):
    from song_database import get_custom_songs

    custom_raw = get_custom_songs(mood_label)
    custom_tracks = []
    for s in custom_raw:
        custom_tracks.append({
            "name": s["name"],
            "artist": s["artist"],
            "album": "Your Custom Pick",
            "url": f"https://www.last.fm/music/{s['artist'].replace(' ', '+').replace('&', 'and')}/_/{s['name'].replace(' ', '+')}",
            "preview_url": None,
            "image": None,
            "duration_ms": 180000,
            "popularity": 100,
        })

    if len(custom_tracks) >= limit:
        return custom_tracks[:limit]

    remaining = limit - len(custom_tracks)
    lastfm_tracks = search_tracks_by_mood(mood_label, limit=remaining)

    return custom_tracks + lastfm_tracks