import requests
import os
from mutagen.flac import FLAC, Picture
from mutagen.easyid3 import EasyID3
from mutagen.id3._frames import APIC
from mutagen.id3 import ID3

def download_image(url) :
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.content

    except Exception as e:
        print(f"下载图片失败: {str(e)}")
        return None

def add_music_tags(file_path, title="", artist="", album="", cover_url=""):
    try:
        if file_path.lower().endswith('.flac'):
            audio = FLAC(file_path)
            audio['title'] = title
            audio['artist'] = artist
            audio['album'] = album
            image_data= download_image(cover_url)
            if image_data :
                audio.clear_pictures()
                picture = Picture()
                picture.type = 3
                picture.desc = 'Cover'
                picture.data = image_data
                audio.add_picture(picture)
            audio.save()

        elif file_path.lower().endswith('.mp3'):
            audio = EasyID3(file_path)
            audio['title'] = title
            audio['artist'] = artist
            audio['album'] = album
            audio.save()
            audio = ID3(file_path)
            image_data= download_image(cover_url)
            if image_data :
                audio['APIC'] = APIC(
                    type=3,
                    encoding=3,
                    desc='Cover',
                    data=image_data
                )
            audio.save(file_path)
        print(f"成功更新文件: {file_path}")
    except Exception as e:
        print(f"处理文件失败: {str(e)}")

def batch_process_songs(songs_list, music_dir):
    for song in songs_list:
        try:
            file_name_mp3 = f"{song['name']} - {song['artist']}.mp3"
            file_name_flac = f"{song['name']} - {song['artist']}.flac"

            file_path_mp3 = os.path.join(music_dir, file_name_mp3)
            file_path_flac = os.path.join(music_dir, file_name_flac)

            if os.path.exists(file_path_mp3):
                add_music_tags(
                    file_path=file_path_mp3,
                    title=song['name'],
                    artist=song['artist'],
                    album=song['album'],
                    cover_url=song['picUrl']
                )
            elif os.path.exists(file_path_flac):
                add_music_tags(
                    file_path=file_path_flac,
                    title=song['name'],
                    artist=song['artist'],
                    album=song['album'],
                    cover_url=song['picUrl']
                )
            else:
                print(f"文件不存在: {file_name_mp3} 或 {file_name_flac}")

        except Exception as e:
            print(f"处理歌曲 {song.get('name', '未知')} 时出错: {str(e)}")
