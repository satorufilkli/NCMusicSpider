def write_links_to_txt(songs_with_url, filename="./download/links.txt"):
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            for song_with_url in songs_with_url:
                url = song_with_url['url']
                if '.mp3' in url.lower():
                    format = '.mp3'
                elif '.flac' in url.lower():
                    format = '.flac'
                else:
                    format = '.mp3'

                file.write(f"{url} ")
                file.write(f"{song_with_url['name']} - {song_with_url['artist']}{format}\n")
                print(f"正在写入歌曲 {song_with_url['name']} 信息")
        print(f"成功将歌曲信息写入 {filename}")

    except Exception as e:
        print(f"写入文件时发生错误: {str(e)}")
