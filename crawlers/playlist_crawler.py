import requests
from urllib.parse import urlencode
from .config import PLAYLIST_API,HEADERS, TIMESTAMP

def get_songs(playlist_id,limit_num=None):
    songs=[]
    params = {
        "id": playlist_id,
        "limit": limit_num,
        "timestamp": TIMESTAMP,
    }

    url = f"{PLAYLIST_API}?{urlencode(params)}"

    try:
        response = requests.post(
            url,
            headers=HEADERS,
        )
        response.raise_for_status()
        data = response.json()
        for i in range (len(data['songs'])):
            song = data
            song = {
                'id': song['songs'][i]['id'],
                'name' : song['songs'][i]['name'],
                'artist' : song['songs'][i]['ar'][0]['name'],
                'album' : song['songs'][i]['al']['name'],
                'picUrl' : song['songs'][i]['al']['picUrl'],
            }
            songs.append(song)
    except Exception as e:
        print(f"Error: {e}")
    return songs
