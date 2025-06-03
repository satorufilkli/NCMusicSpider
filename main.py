import sys
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow
from core.logic import MusicSpiderLogic 
from models.song import Song 
def main():
    app = QApplication(sys.argv)

    # 1. 创建UI和逻辑层的实例
    main_window = MainWindow()
    music_logic = MusicSpiderLogic()

    # 2. 连接 UI 信号到逻辑层槽
    # 当MainWindow请求获取歌单时，调用logic的fetch_playlist方法
    main_window.fetch_playlist_requested.connect(music_logic.fetch_playlist)
    # 当MainWindow请求获取下载链接时，调用logic的get_download_urls方法
    main_window.get_download_urls_requested.connect(music_logic.get_download_urls)
    # 当MainWindow请求保存歌单时，调用logic的save_playlist方法
    main_window.save_playlist_requested.connect(music_logic.save_playlist)
    # 当MainWindow请求加载歌单时，调用logic的load_playlist方法
    main_window.load_playlist_requested.connect(music_logic.load_playlist)


    # 3. 连接逻辑层信号到 UI 层方法
    # 当逻辑层成功获取歌单后，更新UI显示
    music_logic.playlist_fetched_signal.connect(main_window.display_songs)
    # 当逻辑层获取到下载链接后，更新UI表格中的下载链接
    # 注意：logic的download_urls_fetched_signal发出的是list of song_dicts，
    # 其中每个字典已经包含了url和br。我们需要遍历这个列表，逐个更新UI。
    music_logic.download_urls_fetched_signal.connect(
        lambda songs_with_url: [main_window.update_song_download_url(s['id'], s['url'], s['br']) for s in songs_with_url if s.get('url')]
    )
    # 当逻辑层保存歌单成功后，显示提示信息
    music_logic.playlist_saved_signal.connect(lambda msg: main_window.show_message("保存成功", msg))
    # 当逻辑层加载歌单成功后，更新UI显示
    music_logic.playlist_loaded_signal.connect(main_window.display_songs)
    # 当逻辑层发出错误信号时，显示错误信息
    music_logic.error_signal.connect(main_window.show_error)
    # 当逻辑层发出状态更新信号时，更新状态栏
    music_logic.status_signal.connect(main_window.set_status)

    # 4. 显示主窗口
    main_window.show()

    # 5. 启动应用程序事件循环
    sys.exit(app.exec())

if __name__ == "__main__":
    main()