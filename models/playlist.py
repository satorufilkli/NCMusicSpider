from models.song import Song

class Playlist:
    def __init__(self, playlist_id: str, songs: list[Song] = None):
        self.playlist_id = playlist_id
        self.songs = songs if songs else []

    def add_song(self, song: Song):
        self.songs.append(song)

    def to_dict(self):
        return {
            "playlist_id": self.playlist_id,
            "songs": [song.to_dict() for song in self.songs]
        }

    @staticmethod
    def from_dict(data: dict):
        songs = [Song.from_dict(s) for s in data.get("songs", [])]
        return Playlist(playlist_id=data["playlist_id"], songs=songs)
