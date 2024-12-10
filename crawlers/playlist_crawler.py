import requests
from .config import PLAYLIST_API,HEADERS,TIMESTAMP
def get_songs(playlist_id,limit_num=None):
    songs=[]
    payload = {
        "id": playlist_id,
        "limit": limit_num,
        "timestamp": TIMESTAMP,
    }
    try:
        response = requests.post(
            PLAYLIST_API,
            json=payload,
            headers=HEADERS,
        )
        response.raise_for_status()
        data = response.json()
        for i in range (len(data['songs'])):
            song = data['songs'][i]
            song = {
                'id': song['id'],
                'name' : song['name'],
                'artist' : song['ar'][0]['name'],
                'album' : song['al']['name']
            }
            songs.append(song)
    except Exception as e:
        print(f"Error: {e}")
    return songs
