class Song:
    def __init__(self, song_id: str, name: str, artist: str, url: str = ""):
        self.song_id = song_id
        self.name = name
        self.artist = artist 
        self.url = url

    def to_dict(self):
        return {
            "song_id": self.song_id,
            "name": self.name,
            "artist": self.artist,
            "url": self.url
        }

    @staticmethod
    def from_dict(data: dict):
        return Song(
            song_id=data["song_id"],
            name=data["name"],
            artist=data["artist"], 
            url=data.get("url", "")
        )

    def __str__(self):
        return f"{self.name} - {self.artist}"