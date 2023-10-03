import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QListView, QHBoxLayout, QWidget, QPushButton, QFileDialog
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import QUrl, QStringListModel


class VideoPlayerApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Video Player")
        self.setGeometry(100, 100, 1200, 800)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QHBoxLayout(self.central_widget)

        # Create a vertical layout for load and save buttons
        self.buttons_layout = QVBoxLayout()

        self.load_single_button = QPushButton("Load Single Video")
        self.load_single_button.setFixedSize(250, 50)
        self.load_single_button.clicked.connect(self.load_single_video)
        self.buttons_layout.addWidget(self.load_single_button)

        self.load_multiple_button = QPushButton("Load Multiple Videos")
        self.load_multiple_button.setFixedSize(250, 50)
        self.load_multiple_button.clicked.connect(self.load_multiple_videos)
        self.buttons_layout.addWidget(self.load_multiple_button)

        self.save_location_button = QPushButton("Select Save Location")
        self.save_location_button.setFixedSize(250, 50)
        self.save_location_button.clicked.connect(self.select_save_location)
        self.buttons_layout.addWidget(self.save_location_button)

        self.video_list_view = QListView()
        self.video_list_view.setFixedSize(250, 350)
        self.buttons_layout.addWidget(self.video_list_view)

        self.video_list_model = QStringListModel()
        self.video_list_view.setModel(self.video_list_model)

        self.buttons_layout.setSpacing(1)
        self.layout.addLayout(self.buttons_layout)

        # Create a vertical layout for the video player and play button
        self.video_layout = QVBoxLayout()
        self.layout.addLayout(self.video_layout)

        self.video_widget = QVideoWidget()
        self.video_widget.setFixedSize(960, 540)
        self.video_layout.addWidget(self.video_widget)

        self.media_player = QMediaPlayer()
        self.media_player.setVideoOutput(self.video_widget)

        self.play_button = QPushButton("Play")
        self.play_button.clicked.connect(self.play_video)
        self.video_layout.addWidget(self.play_button)

        self.media_content = None

    def play_video(self):
        if self.media_player.state() == QMediaPlayer.PlayingState:
            self.media_player.pause()
            self.play_button.setText("Play")
        else:
            self.media_player.play()
            self.play_button.setText("Pause")

    def load_single_video(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open Video File", "", "Video Files (*.mov *.mp4 *.avi);;All Files (*)", options=options)
        if file_path:
            self.media_content = QMediaContent(QUrl.fromLocalFile(file_path))
            self.media_player.setMedia(self.media_content)
            self.update_video_list(file_path)

    def load_multiple_videos(self):
        options = QFileDialog.Options()
        folder_path = QFileDialog.getExistingDirectory(
            self, "Open Folder", "", options=options)
        if folder_path:
            # Implement logic to load multiple videos from the selected folder
            pass

    def select_save_location(self):
        options = QFileDialog.Options()
        save_folder = QFileDialog.getExistingDirectory(
            self, "Select Save Location", "", options=options)
        if save_folder:
            # Implement logic to save files to the selected location
            pass

    def update_video_list(self, video_name):
        video_names = self.video_list_model.stringList()
        video_names.append(video_name)
        self.video_list_model.setStringList(video_names)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VideoPlayerApp()
    window.show()
    sys.exit(app.exec_())
