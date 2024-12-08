import requests

def get_songs(data):
    songs=[]
    for i in range (len(data['songs'])):
        song = data['songs'][i]
        song = {
            'id': i,
            'name' : song['name'],
            'artist' : song['ar'][0]['name'],
            'album' : song['al']['name']
        }
        songs.append(song)
    return songs

def print_songs_info(songs_info):
    for song_info in songs_info:
        print(f"编号:{song_info['id']}, "
            f"歌曲名:{song_info['name']}, "
            f"歌手:{song_info['artist']}, "
            f"专辑:{song_info['album']}"
        )

url = "https://musicapi.zjgsu-forum.top/playlist/track/all?id=2462787672&limit=3"
response = requests.get(url)
data = response.json()
songs=get_songs(data)
print_songs_info(songs)
