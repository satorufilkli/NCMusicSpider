from src.playlist_crawler import get_songs
from src.dl_urls_crawler import get_dl_urls

def print_songs_info(songs):
    for song in songs:
        print(f"歌曲id:{song['id']}, "
            f"歌曲名:{song['name']}, "
            f"歌手:{song['artist']}, "
            f"专辑:{song['album']}"
        )
def print_dl_urls(dl_urls):
    for dl_url in dl_urls:
        print(
            f"歌曲名:{dl_url['name']}, "
            f"链接:{dl_url['url']}, "
            f"码率:{dl_url['br']}"
        )

def main():
    songs = get_songs(12971562563,5)
    print_dl_urls(get_dl_urls(songs,"exhigh"))

if __name__ == "__main__":
    main()
