import sys
import os
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QListView, QHBoxLayout, QWidget, QPushButton, QFileDialog, QLabel, QMessageBox, QComboBox
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import QUrl, QStringListModel
from PyQt5.QtGui import QFont
import csv


class VideoPlayerApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Volleyball Text Labelling")
        self.setGeometry(100, 100, 1200, 800)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QHBoxLayout(self.central_widget)

        self.buttons_layout = QVBoxLayout()

        self.load_single_button = QPushButton("Open")
        self.load_single_button.setFixedSize(250, 50)
        self.load_single_button.clicked.connect(self.load_single_video)
        self.buttons_layout.addWidget(self.load_single_button)

        self.load_multiple_button = QPushButton("Open Dir")
        self.load_multiple_button.setFixedSize(250, 50)
        self.load_multiple_button.clicked.connect(self.load_multiple_videos)
        self.buttons_layout.addWidget(self.load_multiple_button)

        self.save_location_button = QPushButton("Save Dir")
        self.save_location_button.setFixedSize(250, 50)
        self.save_location_button.clicked.connect(self.select_save_location)
        self.buttons_layout.addWidget(self.save_location_button)

        self.next_video_button = QPushButton("Next Video")
        self.next_video_button.setFixedSize(250, 50)
        self.next_video_button.clicked.connect(self.load_next_video)
        self.buttons_layout.addWidget(self.next_video_button)

        self.previous_video_button = QPushButton("Previous Video")
        self.previous_video_button.setFixedSize(250, 50)
        self.previous_video_button.clicked.connect(self.load_prev_video)
        self.buttons_layout.addWidget(self.previous_video_button)

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

        self.video_title_label = QLabel('')
        self.video_title_label.setFont(QFont('Arial', 20))
        self.video_title_label.setAlignment(QtCore.Qt.AlignCenter)
        self.video_layout.addWidget(self.video_title_label)

        self.video_widget = QVideoWidget()
        self.video_widget.setFixedSize(960, 540)
        self.video_layout.addWidget(self.video_widget)

        self.media_player = QMediaPlayer()
        self.media_player.setVideoOutput(self.video_widget)

        self.play_button = QPushButton("Play")
        self.play_button.clicked.connect(self.play_video)
        self.video_layout.addWidget(self.play_button)

        self.anno_layout = QHBoxLayout()
        self.video_layout.addLayout(self.anno_layout)

        self.annotation_label = QLabel('Current label : ')
        self.annotation_label.setFont(QFont('Arial', 14))
        self.annotation_label.setAlignment(QtCore.Qt.AlignLeft)
        self.anno_layout.addWidget(self.annotation_label)

        self.annotation_text = QLabel('')
        self.annotation_text.setFont(QFont('Arial', 14))
        self.annotation_text.setAlignment(QtCore.Qt.AlignLeft)
        self.anno_layout.addWidget(self.annotation_text)

        self.labelling_layout = QHBoxLayout()
        self.video_layout.addLayout(self.labelling_layout)

        self.setting_position_combobox = QComboBox()
        self.setting_position_combobox.setFixedSize(150, 50)
        self.setting_position_combobox.addItems(
            ['position 1', 'position 2', 'position 3', 'position 4', 'position 5', 'position 6'])
        self.labelling_layout.addWidget(self.setting_position_combobox)
        self.setting_position_combobox.activated.connect(
            self.update_annotation_text)

        self.attacker_combobox = QComboBox()
        self.attacker_combobox.setFixedSize(150, 50)
        self.attacker_combobox.addItems(
            ['outside hitter', 'opposite', 'middle blocker', 'setter', 'libero'])
        self.labelling_layout.addWidget(self.attacker_combobox)
        self.attacker_combobox.activated.connect(
            self.update_annotation_text)

        self.attack_position_combobox = QComboBox()
        self.attack_position_combobox.setFixedSize(150, 50)
        self.attack_position_combobox.addItems(
            ['position 1', 'position 2', 'position 3', 'position 4', 'position 5', 'position 6'])
        self.labelling_layout.addWidget(self.attack_position_combobox)
        self.attack_position_combobox.activated.connect(
            self.update_annotation_text)

        self.point_combobox = QComboBox()
        self.point_combobox.setFixedSize(150, 50)
        self.point_combobox.addItems(
            ['gets', 'loses'])
        self.labelling_layout.addWidget(self.point_combobox)
        self.point_combobox.activated.connect(
            self.update_annotation_text)

        self.attack_method_combobox = QComboBox()
        self.attack_method_combobox.setFixedSize(150, 50)
        self.attack_method_combobox.addItems(
            ['spike', 'A quick', 'B quick', 'C quick', 'D quick', 'back-row spike'])
        self.labelling_layout.addWidget(self.attack_method_combobox)
        self.attack_method_combobox.activated.connect(
            self.update_annotation_text)

        self.media_content = None
        self.current_video_path = None
        self.video_paths = []
        self.current_video_index = 0
        self.save_csv_folder = ''
        self.current_label = ''
        self.out_path = 'label.csv'

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
            self.current_video_path = file_path
            self.media_content = QMediaContent(
                QUrl.fromLocalFile(self.current_video_path))
            self.media_player.setMedia(self.media_content)
            self.update_video_list(file_path)
            self.video_title_label.setText(
                os.path.basename(self.current_video_path))

    def load_multiple_videos(self):
        options = QFileDialog.Options()
        folder_path = QFileDialog.getExistingDirectory(
            self, "Open Folder", "", options=options)

        if folder_path:
            video_files = [f for f in os.listdir(
                folder_path) if f.endswith(('.mov', '.mp4', '.avi'))]
            self.video_paths = [os.path.join(folder_path, video_file)
                                for video_file in video_files]
            self.video_list_model.setStringList(self.video_paths)

            if self.video_paths:
                self.current_video_path = self.video_paths[self.current_video_index]
                self.video_title_label.setText(
                    os.path.basename(self.current_video_path))
                self.media_content = QMediaContent(
                    QUrl.fromLocalFile(self.current_video_path))
                self.media_player.setMedia(self.media_content)

    def select_save_location(self):
        options = QFileDialog.Options()
        save_folder = QFileDialog.getExistingDirectory(
            self, "Select Save Location", "", options=options)
        print(save_folder)
        if save_folder:
            self.save_csv_folder = save_folder
            self.out_path = os.path.join(self.save_csv_folder, 'label.csv')
            with open(self.out_path, 'w', newline='') as csvfile:
                self.writer = csv.writer(csvfile)
                self.writer.writerow(['Video_name', 'Description'])

    def load_next_video(self):
        if len(self.video_paths) > 1 and self.current_video_index < len(self.video_paths)-1:
            self.current_video_index += 1
            self.current_video_path = self.video_paths[self.current_video_index]
            self.video_title_label.setText(
                os.path.basename(self.current_video_path))
            self.media_content = QMediaContent(
                QUrl.fromLocalFile(self.current_video_path))
            self.media_player.setMedia(self.media_content)
        elif self.current_video_index == len(self.video_paths)-1:
            msg_box = QMessageBox()
            msg_box.setWindowTitle('Warning')
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setText('This is the last video in the folder :)')
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.exec()

    def load_prev_video(self):
        if self.current_video_index == 0:
            msg_box = QMessageBox()
            msg_box.setWindowTitle('Warning')
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setText('This is the first video in the folder :)')
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.exec()
        elif len(self.video_paths) > 1 and self.current_video_index > 0 and self.current_video_index < len(self.video_paths):
            self.current_video_index -= 1
            self.current_video_path = self.video_paths[self.current_video_index]
            self.video_title_label.setText(
                os.path.basename(self.current_video_path))
            self.media_content = QMediaContent(
                QUrl.fromLocalFile(self.current_video_path))
            self.media_player.setMedia(self.media_content)
        elif self.current_video_index == 0:
            msg_box = QMessageBox()
            msg_box.setWindowTitle('Warning')
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setText('This is the first video in the folder :)')
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.exec()

    def update_video_list(self, video_name):
        video_names = self.video_list_model.stringList()
        video_names.append(video_name)
        self.video_list_model.setStringList(video_names)

    def update_annotation_text(self):
        self.current_label = 'The setter sets the ball to {}, and the {} from {} {} a point by {}.'.format(self.setting_position_combobox.currentText(
        ), self.attacker_combobox.currentText(), self.attack_position_combobox.currentText(), self.point_combobox.currentText(), self.attack_method_combobox.currentText())
        self.annotation_text.setText(self.current_label)
        print(self.current_label)

        new_data = {
            'Video_name': self.current_video_path,
            'Description': self.current_label
        }

        with open(self.out_path, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            rows = list(reader)

        video_name_to_find = new_data["Video_name"]
        video_name_exists = False

        for row in rows:
            if row["Video_name"] == video_name_to_find:
                row["Description"] = new_data["Description"]
                video_name_exists = True
                break

        if not video_name_exists:
            rows.append(new_data)

        with open(self.out_path, mode='w', newline='') as file:
            fieldnames = ["Video_name", "Description"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            writer.writeheader()
            writer.writerows(rows)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VideoPlayerApp()
    window.show()
    sys.exit(app.exec_())
