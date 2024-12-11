def write_links_to_txt(dl_urls, filename="./download/links.txt"):
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            for dl_url in dl_urls:
                file.write(f"{dl_url['url']} ")
                file.write(f"{dl_url['name']}-{dl_url['artist']}.flac\n")
                print(f"正在写入歌曲 {dl_url['name']} 信息")
        print(f"成功将歌曲信息写入 {filename}")

    except Exception as e:
        print(f"写入文件时发生错误: {str(e)}")
