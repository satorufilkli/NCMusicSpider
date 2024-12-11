import requests
from urllib.parse import urlencode
from .config import DOWNLOAD_API, HEADERS, COOKIE,TIMESTAMP

def get_dl_urls(songs_info,level):
    songs_with_url=[]
    for song in songs_info:
        song_id = song['id']
        song_name = song['name']
        song_artist = song['artist']
        print(f"正在获取{song_name}:{song_id}……")

        params = {
            "id": song_id,
            "level": level,
            "timestamp": TIMESTAMP,
            "cookie": COOKIE
        }

        url = f"{DOWNLOAD_API}?{urlencode(params)}"

        try:
            response = requests.get(
                url,
                headers=HEADERS
            )
            response.raise_for_status()
            data = response.json()
            song_with_url = {
                "name": song_name,
                "artist": song_artist,
                "url": data["data"][0]["url"],
                "br": data["data"][0]["br"]
            }
            songs_with_url.append(song_with_url)
        except requests.exceptions.RequestException as e:
            print(f"Request failed for {song_name}: {e}")
        except (KeyError, IndexError) as e:
            print(f"Failed to parse response for {song_name}: {e}")
        except Exception as e:
            print(f"Unexpected error for {song_name}: {e}")
    return songs_with_url
