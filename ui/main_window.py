from PySide6.QtWidgets import (
    QMainWindow, QVBoxLayout, QHBoxLayout, QWidget,
    QLineEdit, QPushButton, QLabel,
    QFileDialog, QMessageBox, QComboBox, QListWidget, QListWidgetItem,
    QCheckBox, QSizePolicy, QSpacerItem, QGraphicsDropShadowEffect, QApplication
)
from PySide6.QtCore import Qt, Signal, QSize, QBuffer, QByteArray, QUrl
from PySide6.QtGui import QPixmap, QImage, QColor
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply

# 定义一个用于显示单首歌曲信息的卡片Widget
class SongCardWidget(QWidget):

    def __init__(self, song_data: dict, network_manager: QNetworkAccessManager, image_cache: dict):
        super().__init__()
        self.song_data = song_data
        self.network_manager = network_manager
        self.image_cache = image_cache

        self.setStyleSheet("""
            SongCardWidget {
                background-color: #ffffff;
                border: 1px solid #f0f0f0; /* 更细微的边框 */
                border-radius: 10px; /* 适当的圆角 */
            }
            QLabel {
                padding: 2px;
                color: #333;
            }
            QLabel#songName {
                font-weight: bold;
                font-size: 16px;
                color: #2c3e50;
            }
            QLabel#artistAlbum {
                font-size: 13px;
                color: #7f8c8d;
            }
            QLabel#downloadUrl {
                color: #3498db;
                text-decoration: underline;
                font-size: 12px;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
            }
        """)

        shadow_effect = QGraphicsDropShadowEffect(self)
        shadow_effect.setBlurRadius(8) 
        shadow_effect.setColor(QColor(0, 0, 0, 40)) 
        shadow_effect.setOffset(1, 1)

        self.setup_ui()
        self.update_ui_from_data()
        self.load_album_art()

    def setup_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(15, 10, 15, 10)
        main_layout.setSpacing(15)

        left_combined_layout = QHBoxLayout()
        left_combined_layout.setContentsMargins(0,0,0,0)
        left_combined_layout.setSpacing(10) 

        self.checkbox = QCheckBox()
        self.checkbox.setFixedSize(QSize(24, 24))
        left_combined_layout.addWidget(self.checkbox, alignment=Qt.AlignVCenter) # 垂直居中

        self.album_art_label = QLabel()
        self.album_art_label.setFixedSize(QSize(90, 90))
        self.album_art_label.setStyleSheet("border: 1px solid #eee; border-radius: 5px;")
        self.album_art_label.setAlignment(Qt.AlignCenter)
        self.album_art_label.setScaledContents(True)
        left_combined_layout.addWidget(self.album_art_label, alignment=Qt.AlignVCenter) # 垂直居中

        main_layout.addLayout(left_combined_layout)

        # 中间：歌曲信息
        info_layout = QVBoxLayout()
        info_layout.setSpacing(5)
        info_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        self.song_name_label = QLabel(self, objectName="songName")
        self.artist_album_label = QLabel(self, objectName="artistAlbum")
        self.download_url_label = QLabel(self, objectName="downloadUrl")
        self.download_url_label.setWordWrap(True)
        self.download_url_label.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.download_url_label.setOpenExternalLinks(True)

        info_layout.addWidget(self.song_name_label)
        info_layout.addWidget(self.artist_album_label)
        info_layout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))
        info_layout.addWidget(self.download_url_label)
        
        main_layout.addLayout(info_layout)
        
        main_layout.addStretch()

    def update_ui_from_data(self):
        self.song_name_label.setText(self.song_data.get('name', '未知歌曲'))
        artist = self.song_data.get('artist', '未知歌手')
        album = self.song_data.get('album', '未知专辑')
        self.artist_album_label.setText(f"{artist} - {album}")
        
        url = self.song_data.get('url', '')
        br = self.song_data.get('br', '')
        if url:
            self.download_url_label.setText(f'<a href="{url}" style="color:#3498db;">下载链接 ({br}kbps)</a>')
            self.download_url_label.setToolTip(url)
        else:
            self.download_url_label.setText("暂无下载链接")
            self.download_url_label.setToolTip("")

    def load_album_art(self):
        pic_url = self.song_data.get('picUrl')
        if not pic_url:
            self.album_art_label.setText("无封面")
            return

        if pic_url in self.image_cache:
            self.album_art_label.setPixmap(self.image_cache[pic_url])
            return

        self.album_art_label.setText("加载中...")
        self.album_art_label.setPixmap(QPixmap())

        request = QNetworkRequest(QUrl(pic_url))
        reply = self.network_manager.get(request)
        reply.finished.connect(lambda: self._image_download_finished(reply, pic_url))

    def _image_download_finished(self, reply: QNetworkReply, url: str):
        if reply.error() == QNetworkReply.NoError:
            image_data = reply.readAll()
            image = QImage()
            if image.loadFromData(image_data):
                pixmap = QPixmap.fromImage(image)
                scaled_pixmap = pixmap.scaled(self.album_art_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.album_art_label.setPixmap(scaled_pixmap)
                self.image_cache[url] = scaled_pixmap
                self.album_art_label.setText("")
            else:
                self.album_art_label.setText("加载失败")
        else:
            self.album_art_label.setText("加载失败")
            print(f"Error loading image {url}: {reply.errorString()}")
        reply.deleteLater()

    def get_song_id(self):
        return self.song_data.get('id')

    def get_song_data(self):
        return self.song_data

    def is_checked(self):
        
        return self.checkbox.isChecked()
    
    def set_checked(self, checked: bool):
        print(f"SongCardWidget '{self.song_data.get('name')}' - Setting checkbox to: {checked}") # Debugging line
        self.checkbox.blockSignals(True) 
        self.checkbox.setChecked(checked)
        self.checkbox.blockSignals(False)
        print(f"SongCardWidget '{self.song_data.get('name')}' - Checkbox actual state: {self.checkbox.isChecked()}") # Debugging line


    def update_download_url_and_br(self, url: str, br: int):
        self.song_data['url'] = url
        self.song_data['br'] = br
        if url:
            self.download_url_label.setText(f'<a href="{url}" style="color:#3498db;">下载链接 ({br}kbps)</a>')
            self.download_url_label.setToolTip(url)
        else:
            self.download_url_label.setText("获取链接失败")
            self.download_url_label.setToolTip("")


class MainWindow(QMainWindow):
    fetch_playlist_requested = Signal(str)
    get_download_urls_requested = Signal(list, str)
    save_playlist_requested = Signal(list, str)
    load_playlist_requested = Signal(str)

    MUSIC_QUALITY_LEVELS = {
        "标准 (standard)": "standard",
        "较高 (higher)": "higher",
        "极高 (exhigh)": "exhigh",
        "无损 (lossless)": "lossless",
        "Hi-Res (hires)": "hires",
        "高清环绕声 (jyeffect)": "jyeffect",
        "沉浸环绕声 (sky)": "sky",
        "杜比全景声 (dolby)": "dolby",
        "超清母带 (jymaster)": "jymaster"
    }

    def __init__(self):
        super().__init__()
        self.setWindowTitle("NCMusicSpider ")
        self.setGeometry(100, 100, 950, 750) # 调整默认界面大小，稍微增大以便容纳卡片间距

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)

        self.network_manager = QNetworkAccessManager(self)
        self.image_cache = {}

        self.setup_ui()
        self.current_playlist_id = None
        self.current_songs_data = []

    def setup_ui(self):
        # 歌单ID输入和获取按钮
        input_layout = QHBoxLayout()
        self.playlist_id_label = QLabel("歌单ID:")
        self.playlist_id_input = QLineEdit()
        self.playlist_id_input.setPlaceholderText("请输入歌单ID")
        self.playlist_id_input.setMaximumWidth(350) # 限制输入框的宽度，稍微放宽
        self.fetch_playlist_button = QPushButton("获取歌单")
        self.fetch_playlist_button.clicked.connect(self._on_fetch_playlist_clicked)

        input_layout.addWidget(self.playlist_id_label)
        input_layout.addWidget(self.playlist_id_input)
        input_layout.addWidget(self.fetch_playlist_button)
        input_layout.addStretch() # 将元素推到左侧
        self.main_layout.addLayout(input_layout)

        # 歌曲列表
        self.songs_list_widget = QListWidget()
        self.songs_list_widget.setSelectionMode(QListWidget.NoSelection)
        self.songs_list_widget.setSpacing(10) # 设置卡片之间的间隔
        self.main_layout.addWidget(self.songs_list_widget)

        # 控制按钮和音质选择
        control_layout = QHBoxLayout()
        
        self.quality_label = QLabel("选择音质:")
        self.quality_combo_box = QComboBox()
        for display_name, level_key in self.MUSIC_QUALITY_LEVELS.items():
            self.quality_combo_box.addItem(display_name, level_key)
        self.quality_combo_box.setCurrentIndex(2) # 默认选中 'exhigh'

        control_layout.addWidget(self.quality_label)
        control_layout.addWidget(self.quality_combo_box)
        
        self.get_download_links_button = QPushButton("获取选中歌曲下载链接")
        self.get_download_links_button.clicked.connect(self._on_get_download_links_clicked)
        self.get_all_download_links_button = QPushButton("获取所有歌曲下载链接")
        self.get_all_download_links_button.clicked.connect(self._on_get_all_download_links_clicked)

        control_layout.addWidget(self.get_download_links_button)
        control_layout.addWidget(self.get_all_download_links_button)
        
        control_layout.addStretch() # 将保存/加载按钮推到右侧

        self.save_playlist_button = QPushButton("保存歌单")
        self.save_playlist_button.clicked.connect(self._on_save_playlist_clicked)
        self.load_playlist_button = QPushButton("加载歌单")
        self.load_playlist_button.clicked.connect(self._on_load_playlist_clicked)

        control_layout.addWidget(self.save_playlist_button)
        control_layout.addWidget(self.load_playlist_button)
        self.main_layout.addLayout(control_layout)

        self.status_label = QLabel("准备就绪...")
        self.main_layout.addWidget(self.status_label)

    def _on_fetch_playlist_clicked(self):
        playlist_id = self.playlist_id_input.text().strip()
        if not playlist_id:
            self.show_message("错误", "请输入歌单ID！")
            return
        self.set_status(f"正在获取歌单 {playlist_id}...")
        self.fetch_playlist_requested.emit(playlist_id)

    def _get_selected_songs_data(self):
        selected_songs = []
        for i in range(self.songs_list_widget.count()):
            list_item = self.songs_list_widget.item(i)
            card_widget = self.songs_list_widget.itemWidget(list_item)
            if isinstance(card_widget, SongCardWidget) and card_widget.is_checked():
                selected_songs.append(card_widget.get_song_data())
        return selected_songs

    def _on_get_download_links_clicked(self):
        songs_to_get_url = self._get_selected_songs_data()
        if not songs_to_get_url:
            self.show_message("提示", "请先选择要获取下载链接的歌曲！")
            return

        selected_level = self.quality_combo_box.currentData()
        self.set_status(f"正在获取选中歌曲的 {selected_level} 下载链接...")
        self.get_download_urls_requested.emit(songs_to_get_url, selected_level)

    def _on_get_all_download_links_clicked(self):
        if not self.current_songs_data:
            self.show_message("提示", "请先获取歌单！")
            return

        selected_level = self.quality_combo_box.currentData()
        self.set_status(f"正在获取所有歌曲的 {selected_level} 下载链接...")
        self.get_download_urls_requested.emit(self.current_songs_data, selected_level)

    def _on_save_playlist_clicked(self):
        if not self.current_songs_data:
            self.show_message("提示", "没有歌单可以保存！")
            return

        file_path, _ = QFileDialog.getSaveFileName(self, "保存歌单", "", "JSON Files (*.json);;All Files (*)")
        if file_path:
            self.save_playlist_requested.emit(self.current_songs_data, file_path)
            self.set_status(f"歌单将保存到 {file_path}...")

    def _on_load_playlist_clicked(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "加载歌单", "", "JSON Files (*.json);;All Files (*)")
        if file_path:
            self.set_status(f"正在从 {file_path} 加载歌单...")
            self.load_playlist_requested.emit(file_path)


    def display_songs(self, songs_info: list):
        """
        在QListWidget中显示歌曲信息卡片。
        此方法会在外部（如MusicLogic）获取到歌单数据后被调用。
        """
        print(f"Displaying {len(songs_info)} songs.") # Debugging line
        self.songs_list_widget.clear()
        self.current_songs_data = songs_info

        if not songs_info:
            self.set_status("未找到歌曲。") 
            return

        for song_data in songs_info:
            card_widget = SongCardWidget(song_data, self.network_manager, self.image_cache)
            
            list_item = QListWidgetItem(self.songs_list_widget)
            # 调整 item 的 sizeHint 以适应卡片内容和间距
            list_item.setSizeHint(card_widget.sizeHint().expandedTo(QSize(0, 120))) # 确保高度足够
            
            self.songs_list_widget.addItem(list_item)
            self.songs_list_widget.setItemWidget(list_item, card_widget)

        self.set_status(f"已显示 {len(songs_info)} 歌曲。")


    def update_song_download_url(self, song_id: str, download_url: str, br: int):
        """
        根据歌曲ID更新对应卡片的下载链接和码率。
        此方法会在外部（如MusicLogic）获取到下载链接后被调用。
        """
        print(f"Attempting to update song ID: {song_id} with URL: {download_url}") # Debugging line
        found = False
        for i in range(self.songs_list_widget.count()):
            list_item = self.songs_list_widget.item(i)
            card_widget = self.songs_list_widget.itemWidget(list_item)
            
            if isinstance(card_widget, SongCardWidget) and str(card_widget.get_song_id()) == str(song_id):
                card_widget.update_download_url_and_br(download_url, br)
                found = True
                break
        
        # 同时更新 current_songs_data 列表中的数据，以便保存歌单时包含最新链接
        for s_data in self.current_songs_data:
            if str(s_data.get('id')) == str(song_id):
                s_data['url'] = download_url
                s_data['br'] = br
                break

        if found:
            self.set_status(f"歌曲 ID {song_id} 的下载链接已更新。")
        else:
            self.set_status(f"警告: 未找到歌曲 ID {song_id} 对应的卡片。")


    def set_status(self, message):
        """更新状态栏文本。"""
        self.status_label.setText(message)

    def show_message(self, title, message):
        """显示信息对话框。"""
        QMessageBox.information(self, title, message)

    def show_error(self, title, message):
        """显示错误对话框。"""
        QMessageBox.critical(self, title, message)