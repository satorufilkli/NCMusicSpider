import requests

from .config import DOWNLOAD_API, HEADERS, COOKIE,TIMESTAMP
def get_dl_urls(songs,level):
    dl_urls=[]
    for song in songs:
        song_id = song['id']
        song_name = song['name']
        print(f"正在获取“{song_name}”……")
        payload = {
            "id": song_id,
            "level": level,
            "timestamp": TIMESTAMP,
            "cookie" : COOKIE
        }
        try:
            response = requests.post(
                DOWNLOAD_API,
                json=payload,
                headers=HEADERS,
            )
            response.raise_for_status()
            data = response.json()
            dl_url = {
                "name" : song_name,
                "url" : data["data"][0]["url"],
                "br" : data["data"][0]["br"]
            }
            dl_urls.append(dl_url)
        except requests.exceptions.RequestException as e:
            print(f"Request failed for {song_name}: {e}")
        except (KeyError, IndexError) as e:
            print(f"Failed to parse response for {song_name}: {e}")
        except Exception as e:
            print(f"Unexpected error for {song_name}: {e}")
    return dl_urls
