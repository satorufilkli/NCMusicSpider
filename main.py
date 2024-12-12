from crawlers.playlist_crawler import get_songs
from crawlers.dl_urls_crawler import get_dl_urls
from download.write_links import write_links_to_txt
from save_to_json import save_to_json
from add_music_tags import batch_process_songs

def main():
    playlist_id = input("请输入歌单ID：")
    songs_info = get_songs(playlist_id)

    songs_with_url = get_dl_urls(songs_info,"lossless")
    save_to_json(songs_with_url,"songs_list.json")
    write_links_to_txt(songs_with_url)
    # batch_process_songs(songs_info,"./download/musics")

if __name__ == "__main__":
    main()
