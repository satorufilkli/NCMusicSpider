import requests
from urllib.parse import urlencode
from .config import DOWNLOAD_API, PLAYLIST_API, HEADERS
def get_songs_from_api(playlist_id, limit_num=None):
    songs = []
    params = {
        "id": playlist_id,
        "limit": limit_num,
    }
    url = f"{PLAYLIST_API}?{urlencode(params)}"
    try:
        response = requests.post(url, headers=HEADERS)
        response.raise_for_status()
        data = response.json()
        for i in range(len(data['songs'])):
            song = {
                'id': data['songs'][i]['id'],
                'name': data['songs'][i]['name'],
                'artist': data['songs'][i]['ar'][0]['name'],
                'album': data['songs'][i]['al']['name'],
                'picUrl': data['songs'][i]['al']['picUrl'],
            }
            songs.append(song)
    except Exception as e:
        print(f"Error fetching songs: {e}")
    return songs


def get_download_urls(songs_info, level):
    songs_with_url = []
    for song in songs_info:
        song_id = song['id']
        song_name = song['name']
        song_artist = song['artist']
        song_picUrl = song['picUrl']
        print(f"Getting download URL for {song_name} (ID: {song_id})...")

        params = {
            "id": song_id,
            "level": level,
        }

        url = f"{DOWNLOAD_API}?{urlencode(params)}"
        try:
            response = requests.get(url, headers=HEADERS)
            response.raise_for_status()
            data = response.json()
            url = data["data"][0]["url"] if data["data"] else None
            br = data["data"][0]["br"] if data["data"] else None

            if url:
                songs_with_url.append({
                    "id": song_id,
                    "name": song_name,
                    "artist": song_artist,
                    "picUrl": song_picUrl,
                    "url": url,
                    "br": br,
                })
            else:
                print(f"No download URL found for {song_name}")
        except Exception as e:
            print(f"Failed to get download URL for {song_name}: {e}")

    return songs_with_url
