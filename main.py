from crawlers.playlist_crawler import get_songs
from crawlers.dl_urls_crawler import get_dl_urls
from save_to_json import save_to_json

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
    songs = get_songs(12971562563)
    save_to_json(songs)
    # save_to_json(get_dl_urls(songs,"hires"))

if __name__ == "__main__":
    main()
