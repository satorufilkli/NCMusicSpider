import json
from models.playlist import Playlist

def save_playlist_to_file(playlist: Playlist, path: str):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(playlist.to_dict(), f, ensure_ascii=False, indent=2)

def load_playlist_from_file(path: str) -> Playlist:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
        return Playlist.from_dict(data)
