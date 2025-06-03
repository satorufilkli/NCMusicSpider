from PySide6.QtCore import QObject, Signal, QRunnable, Slot, QThreadPool
import traceback
import sys

from crawlers.nc_crawler import get_songs_from_api, get_download_urls
from models.playlist import Playlist
from models.song import Song
from utils.io import save_playlist_to_file, load_playlist_from_file

# 用于在后台执行耗时操作的Worker
class Worker(QRunnable):
    def __init__(self, fn, *args, **kwargs):
        super().__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

    @Slot()
    def run(self):
        try:
            result = self.fn(*self.args, **self.kwargs)
            self.signals.result.emit(result)
        except Exception as e:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        finally:
            self.signals.finished.emit()

class WorkerSignals(QObject):
    result = Signal(object)
    error = Signal(tuple)
    finished = Signal()
    status = Signal(str)


class MusicSpiderLogic(QObject):
    # 定义信号，用于将处理结果和状态更新发送给UI层
    playlist_fetched_signal = Signal(list) # 参数: 歌曲信息列表
    download_urls_fetched_signal = Signal(list) # 参数: 包含URL的歌曲信息列表
    playlist_saved_signal = Signal(str) # 参数: 保存成功消息
    playlist_loaded_signal = Signal(list) # 参数: 加载的歌曲信息列表
    error_signal = Signal(str, str) # 参数: 错误标题, 错误信息
    status_signal = Signal(str) # 参数: 状态信息

    def __init__(self):
        super().__init__()
        self.threadpool = QThreadPool() # QThreadPool用于管理后台任务
        print(f"Multithreading with maximum {self.threadpool.maxThreadCount()} threads")

    @Slot(str)
    def fetch_playlist(self, playlist_id: str):
        self.status_signal.emit(f"正在后台获取歌单 {playlist_id}...")

        worker = Worker(self._fetch_playlist_task, playlist_id)
        worker.signals.result.connect(self._handle_playlist_fetched)
        worker.signals.error.connect(self._handle_error)
        worker.signals.finished.connect(lambda: self.status_signal.emit("歌单获取任务完成。"))
        self.threadpool.start(worker)

    def _fetch_playlist_task(self, playlist_id: str):
        """实际执行获取歌单的任务（在后台线程中）"""
        songs_info = get_songs_from_api(playlist_id)
        if songs_info:
            return songs_info
        else:
            raise Exception("获取歌单失败，请检查歌单ID或网络连接。")

    def _handle_playlist_fetched(self, songs_info: list):
        """处理获取歌单任务的结果"""
        self.playlist_fetched_signal.emit(songs_info)
        self.status_signal.emit(f"成功获取 {len(songs_info)} 歌曲。")

    @Slot(list, str)
    def get_download_urls(self, songs_info: list, level: str):
        self.status_signal.emit(f"正在后台获取下载链接 ({level} 音质)...")

        worker = Worker(self._get_download_urls_task, songs_info, level)
        worker.signals.result.connect(self._handle_download_urls_fetched)
        worker.signals.error.connect(self._handle_error)
        worker.signals.finished.connect(lambda: self.status_signal.emit("下载链接获取任务完成。"))
        self.threadpool.start(worker)

    def _get_download_urls_task(self, songs_info: list, level: str):
        """实际执行获取下载链接的任务（在后台线程中）"""
        songs_with_url = get_download_urls(songs_info, level)
        return songs_with_url

    def _handle_download_urls_fetched(self, songs_with_url: list):
        """处理获取下载链接任务的结果"""
        self.download_urls_fetched_signal.emit(songs_with_url)
        self.status_signal.emit(f"已获取 {len(songs_with_url)} 歌曲的下载链接。")

    @Slot(object, str)
    def save_playlist(self, songs_data: list, file_path: str):
        self.status_signal.emit(f"正在后台保存歌单到 {file_path}...")
        
        # 将歌曲字典列表转换为 Playlist 对象
        songs = []
        for song_dict in songs_data:
            songs.append(Song(
                song_id=str(song_dict['id']),
                name=song_dict['name'],
                artist=song_dict['artist'],
                url=song_dict.get('url', '')
            ))
        temp_playlist_id = "saved_playlist" # 占位符
        playlist = Playlist(playlist_id=temp_playlist_id, songs=songs)

        worker = Worker(save_playlist_to_file, playlist, file_path)
        worker.signals.result.connect(lambda: self._handle_playlist_saved(file_path))
        worker.signals.error.connect(self._handle_error)
        worker.signals.finished.connect(lambda: self.status_signal.emit("歌单保存任务完成。"))
        self.threadpool.start(worker)

    def _handle_playlist_saved(self, file_path: str):
        """处理保存歌单任务的结果"""
        self.playlist_saved_signal.emit(f"歌单已成功保存到: {file_path}")
        self.status_signal.emit("歌单保存成功。")

    @Slot(str)
    def load_playlist(self, file_path: str):
        self.status_signal.emit(f"正在后台从 {file_path} 加载歌单...")

        worker = Worker(load_playlist_from_file, file_path)
        worker.signals.result.connect(self._handle_playlist_loaded)
        worker.signals.error.connect(self._handle_error)
        worker.signals.finished.connect(lambda: self.status_signal.emit("歌单加载任务完成。"))
        self.threadpool.start(worker)

    def _handle_playlist_loaded(self, playlist: Playlist):
        """处理加载歌单任务的结果"""
        songs_info = [song.to_dict() for song in playlist.songs]
        self.playlist_loaded_signal.emit(songs_info)
        self.status_signal.emit(f"歌单已成功从 {playlist.playlist_id} 加载，包含 {len(songs_info)} 歌曲。")

    def _handle_error(self, error_tuple):
        """处理所有后台任务的错误"""
        exctype, value, tb_str = error_tuple
        error_title = "操作失败"
        error_message = f"发生错误: {value}\n\n详细信息:\n{tb_str}"
        self.error_signal.emit(error_title, error_message)
        self.status_signal.emit(f"发生错误: {value}")
        print(f"Error caught in logic: {value}\n{tb_str}") # 打印到控制台方便调试