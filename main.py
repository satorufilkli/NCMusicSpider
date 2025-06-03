import sys
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow
from core.logic import MusicSpiderLogic 
from models.song import Song 
def main():
    app = QApplication(sys.argv)

    # 创建UI和逻辑层的实例
    main_window = MainWindow()
    music_logic = MusicSpiderLogic()

    # 连接 UI 信号到逻辑层槽
    main_window.fetch_playlist_requested.connect(music_logic.fetch_playlist)
    main_window.get_download_urls_requested.connect(music_logic.get_download_urls)
    main_window.save_playlist_requested.connect(music_logic.save_playlist)
    main_window.load_playlist_requested.connect(music_logic.load_playlist)


    # 连接逻辑层信号到 UI 层方法
    music_logic.playlist_fetched_signal.connect(main_window.display_songs)
    music_logic.download_urls_fetched_signal.connect(
        lambda songs_with_url: [main_window.update_song_download_url(s['id'], s['url'], s['br']) for s in songs_with_url if s.get('url')]
    )
    music_logic.playlist_saved_signal.connect(lambda msg: main_window.show_message("保存成功", msg))
    music_logic.playlist_loaded_signal.connect(main_window.display_songs)
    music_logic.error_signal.connect(main_window.show_error)
    music_logic.status_signal.connect(main_window.set_status)

    main_window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()