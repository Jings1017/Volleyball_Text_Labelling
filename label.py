import sys
import os
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QListWidget, QListWidgetItem, QSlider, QStyle, QHBoxLayout, QWidget, QPushButton, QFileDialog, QLabel, QMessageBox, QComboBox
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import QUrl, Qt, QSize
from PyQt5.QtGui import QFont, QColor, QPalette
import csv
import json

style = """QSlider::groove:horizontal {
border: 1px solid #999999;
height: 20px; /* the groove expands to the size of the slider by default. by giving it a height, it has a fixed size */
}
QSlider::handle:horizontal {
background: #fff;
width: 10px;
margin: -1px -1px;
border: 1px solid #6FC1FF;
}
QSlider::handle:horizontal:hover {
background: #000;
border-color: #000;
}
QSlider::add-page:horizontal {
background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #B1B1B1, stop:1 #c4c4c4);
}
QSlider::sub-page:horizontal{
background: #6FC1FF
}
"""


class VolleyballLabel(QMainWindow):
    def __init__(self):
        super().__init__()

        with open('./data.json') as f:
            self.data = json.load(f)

        self.setWindowTitle("Volleyball Text Labelling")
        self.setGeometry(100, 100, 1700, 900)
        self.setFixedSize(1700, 900)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout = QHBoxLayout(self.central_widget)

        ### LEFT layout ###

        self.left_layout_component_init()

        self.buttons_layout = QVBoxLayout()
        self.buttons_layout.addWidget(self.load_multiple_button)
        self.buttons_layout.addWidget(self.save_location_button)
        self.buttons_layout.addWidget(self.next_video_button)
        self.buttons_layout.addWidget(self.previous_video_button)
        self.buttons_layout.addWidget(self.listWidget)
        self.buttons_layout.addWidget(self.done_button)
        self.layout.addLayout(self.buttons_layout)

        ### RIGHT layout ###

        self.right_layout_component_init()

        self.video_layout = QVBoxLayout()
        self.layout.addLayout(self.video_layout)

        self.video_layout.addWidget(self.video_title_label)
        self.video_layout.addWidget(self.video_widget)

        self.controlLayout = QHBoxLayout()
        self.controlLayout.addWidget(self.playButton)
        self.controlLayout.addWidget(self.positionSlider)

        self.video_layout.addLayout(self.controlLayout)
        self.video_layout.addWidget(self.original_text)
        self.video_layout.addWidget(self.annotation_text)

        self.custom_choose_layout = QHBoxLayout()
        self.custom_choose_layout.addLayout(self.setting_position_layout)
        self.custom_choose_layout.addLayout(self.attacker_layout)
        self.custom_choose_layout.addLayout(self.attack_position_layout)
        self.custom_choose_layout.addLayout(self.point_layout)
        self.custom_choose_layout.addLayout(self.attack_method_layout)
        self.video_layout.addLayout(self.custom_choose_layout)

        self.media_player.setVideoOutput(self.video_widget)
        self.media_player.stateChanged.connect(self.mediaStateChanged)
        self.media_player.positionChanged.connect(self.positionChanged)
        self.media_player.durationChanged.connect(self.durationChanged)
        self.media_player.error.connect(self.handleError)

        self.media_content = None
        self.folder_path = ''
        self.current_video_path = None
        self.video_paths = []
        self.current_video_index = 0
        self.save_csv_folder = ''
        self.current_label = ''
        self.out_path = 'label.csv'

    def left_layout_component_init(self):
        self.load_multiple_button = QPushButton("Open Dir")
        self.load_multiple_button.setFixedSize(300, 50)
        self.load_multiple_button.clicked.connect(self.load_multiple_videos)

        self.save_location_button = QPushButton("Save Dir")
        self.save_location_button.setFixedSize(300, 50)
        self.save_location_button.clicked.connect(self.select_save_location)

        self.next_video_button = QPushButton("Next Video")
        self.next_video_button.setFixedSize(300, 50)
        self.next_video_button.clicked.connect(self.load_next_video)

        self.previous_video_button = QPushButton("Previous Video")
        self.previous_video_button.setFixedSize(300, 50)
        self.previous_video_button.clicked.connect(self.load_prev_video)

        self.listWidget = QListWidget(self)
        self.listWidget.setFixedSize(300, 500)

        self.done_button = QPushButton("Save")
        self.done_button.setFixedSize(300, 50)
        self.done_button.clicked.connect(self.save_current_data)

    def right_layout_component_init(self):
        self.video_title_label = QLabel('')
        self.video_title_label.setFont(QFont('Arial', 20))
        self.video_title_label.setAlignment(QtCore.Qt.AlignCenter)

        self.video_widget = QVideoWidget()
        self.video_widget.setFixedSize(1400, 500)

        self.media_player = QMediaPlayer()
        self.media_player.setVideoOutput(self.video_widget)

        btnSize = QSize(25, 25)
        self.playButton = QPushButton()
        self.playButton.setEnabled(False)
        self.playButton.setFixedHeight(25)
        self.playButton.setIconSize(btnSize)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.play)

        self.positionSlider = QSlider(Qt.Horizontal)
        self.positionSlider.setRange(0, 0)
        self.positionSlider.setStyleSheet(style)

        self.positionSlider.sliderMoved.connect(self.setPosition)

        self.original_text = QLabel('Original label :')
        self.original_text.setFont(QFont('Arial', 12))
        self.original_text.setAlignment(
            QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)

        self.annotation_text = QLabel('Current label :')
        self.annotation_text.setFont(QFont('Arial', 12))
        self.annotation_text.setAlignment(
            QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)

        self.combo_layout_component_init()

    def combo_layout_component_init(self):

        self.setting_position_layout = QVBoxLayout()
        self.setting_position_text = QLabel('Setting Position')
        self.setting_position_text.setFont(QFont('Arial', 12))
        self.setting_position_text.setAlignment(QtCore.Qt.AlignCenter)
        self.setting_position_layout.addWidget(self.setting_position_text)

        self.setting_position_combobox = QComboBox()
        self.setting_position_combobox.setFixedSize(250, 50)
        self.setting_position_combobox.addItems(self.data['position'])
        self.setting_position_layout.addWidget(self.setting_position_combobox)
        self.setting_position_combobox.activated.connect(
            self.update_annotation_text)

        # ----
        self.attacker_layout = QVBoxLayout()
        self.attacker_text = QLabel('Attacker')
        self.attacker_text.setFont(QFont('Arial', 12))
        self.attacker_text.setAlignment(QtCore.Qt.AlignCenter)
        self.attacker_layout.addWidget(self.attacker_text)

        self.attacker_combobox = QComboBox()
        self.attacker_combobox.setFixedSize(150, 50)
        self.attacker_combobox.addItems(self.data['attacker'])
        self.attacker_layout.addWidget(self.attacker_combobox)
        self.attacker_combobox.activated.connect(
            self.update_annotation_text)

        # ----
        self.attack_position_layout = QVBoxLayout()
        self.attacker_position_text = QLabel('Attacker Position')
        self.attacker_position_text.setFont(QFont('Arial', 12))
        self.attacker_position_text.setAlignment(QtCore.Qt.AlignCenter)
        self.attack_position_layout.addWidget(self.attacker_position_text)

        self.attack_position_combobox = QComboBox()
        self.attack_position_combobox.setFixedSize(250, 50)
        self.attack_position_combobox.addItems(self.data['position'])
        self.attack_position_layout.addWidget(self.attack_position_combobox)
        self.attack_position_combobox.activated.connect(
            self.update_annotation_text)

        # ----
        self.point_layout = QVBoxLayout()
        self.point_text = QLabel('Get/Lose')
        self.point_text.setFont(QFont('Arial', 12))
        self.point_text.setAlignment(QtCore.Qt.AlignCenter)
        self.point_layout.addWidget(self.point_text)

        self.point_combobox = QComboBox()
        self.point_combobox.setFixedSize(150, 50)
        self.point_combobox.addItems(
            ['gets', 'loses'])
        self.point_layout.addWidget(self.point_combobox)
        self.point_combobox.activated.connect(
            self.update_annotation_text)

        # ----
        self.attack_method_layout = QVBoxLayout()
        self.attack_method_text = QLabel('Attack Method')
        self.attack_method_text.setFont(QFont('Arial', 12))
        self.attack_method_text.setAlignment(QtCore.Qt.AlignCenter)
        self.attack_method_layout.addWidget(self.attack_method_text)

        self.attack_method_combobox = QComboBox()
        self.attack_method_combobox.setFixedSize(150, 50)
        self.attack_method_combobox.addItems(self.data['attack_method'])
        self.attack_method_layout.addWidget(self.attack_method_combobox)
        self.attack_method_combobox.activated.connect(
            self.update_annotation_text)

    def play(self):
        if self.media_player.state() == QMediaPlayer.PlayingState:
            self.media_player.pause()
        else:
            self.media_player.play()

    def mediaStateChanged(self, state):
        if self.media_player.state() == QMediaPlayer.PlayingState:
            self.playButton.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playButton.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPlay))

    def positionChanged(self, position):
        self.positionSlider.setValue(position)

    def durationChanged(self, duration):
        self.positionSlider.setRange(0, duration)

    def setPosition(self, position):
        self.media_player.setPosition(position)

    def handleError(self):
        self.playButton.setEnabled(False)
        # self.statusBar.showMessage("Error: " + self.media_player.errorString())

    def save_current_data(self):

        blue_color = QColor(0, 0, 255)
        palette = QPalette()
        palette.setColor(QPalette.WindowText, blue_color)
        self.annotation_text.setPalette(palette)

        new_data = {
            'Video_name': os.path.basename(self.current_video_path),
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
            for row in rows:
                writer.writerow(row)

        for i in range(self.listWidget.count()):
            item = self.listWidget.item(i)
            for row in rows:
                if row["Video_name"] == item.text():
                    item.setBackground(QColor(124, 232, 249))

    def load_multiple_videos(self):
        options = QFileDialog.Options()
        self.folder_path = QFileDialog.getExistingDirectory(
            self, "Open Folder", "", options=options)

        if self.folder_path:
            video_files = [f for f in os.listdir(
                self.folder_path) if f.endswith(('.mov', '.mp4', '.avi'))]
            self.video_paths = [os.path.join(self.folder_path, video_file)
                                for video_file in video_files]

            self.show_video_names = [os.path.basename(
                video_path) for video_path in self.video_paths]

            with open(self.out_path, mode='r', newline='') as file:
                reader = csv.DictReader(file)
                rows = list(reader)

            for item_text in self.show_video_names:
                item = QListWidgetItem(item_text)
                for row in rows:
                    if row["Video_name"] == item_text:
                        item.setBackground(QColor(124, 232, 249))
                is_exist = False
                for index in range(self.listWidget.count()):
                    it = self.listWidget.item(index)
                    if it.text() == item_text:
                        is_exist = True
                if not is_exist:
                    self.listWidget.addItem(item)

            self.listWidget.itemClicked.connect(self.itemClickedHandler)

            if self.video_paths:
                self.playButton.setEnabled(True)
                self.current_video_path = self.video_paths[self.current_video_index]
                self.video_title_label.setText(
                    os.path.basename(self.current_video_path))
                self.media_content = QMediaContent(
                    QUrl.fromLocalFile(self.current_video_path))
                self.media_player.setMedia(self.media_content)
                self.update_original_text()

        else:
            msg_box = QMessageBox()
            msg_box.setWindowTitle('Warning')
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setText('The Dir is empty !')
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.exec()

    def itemClickedHandler(self, item):

        black_color = QColor(0, 0, 0)
        palette = QPalette()
        palette.setColor(QPalette.WindowText, black_color)
        self.annotation_text.setPalette(palette)

        self.current_video_path = os.path.join(self.folder_path, item.text())

        self.video_title_label.setText(
            os.path.basename(self.current_video_path))
        self.media_content = QMediaContent(
            QUrl.fromLocalFile(self.current_video_path))
        self.media_player.setMedia(self.media_content)
        self.update_original_text()

    def select_save_location(self):
        options = QFileDialog.Options()
        save_folder = QFileDialog.getExistingDirectory(
            self, "Select Save Location", "", options=options)
        if save_folder:
            self.save_csv_folder = save_folder
            self.out_path = os.path.join(self.save_csv_folder, 'label.csv')

        with open(self.out_path, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            rows = list(reader)

        for i in range(self.listWidget.count()):
            item = self.listWidget.item(i)
            for row in rows:
                if row["Video_name"] == item.text():
                    item.setBackground(QColor(124, 232, 249))

    def load_next_video(self):
        black_color = QColor(0, 0, 0)
        palette = QPalette()
        palette.setColor(QPalette.WindowText, black_color)
        self.annotation_text.setPalette(palette)

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

        self.update_original_text()

    def load_prev_video(self):
        black_color = QColor(0, 0, 0)
        palette = QPalette()
        palette.setColor(QPalette.WindowText, black_color)
        self.annotation_text.setPalette(palette)

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

        self.update_original_text()

    def update_annotation_text(self):
        text = ''
        if 'and' in self.setting_position_combobox.currentText():
            text = 'The setter sets the ball between {}, '.format(
                self.setting_position_combobox.currentText())
        else:
            text = 'The setter sets the ball to {}, '.format(
                self.setting_position_combobox.currentText())
        if 'and' in self.attack_position_combobox.currentText():
            text += 'and the {} between {} {} a point by {}.'.format(self.attacker_combobox.currentText(
            ), self.attack_position_combobox.currentText(), self.point_combobox.currentText(), self.attack_method_combobox.currentText())
        else:
            text += 'and the {} from {} {} a point by {}.'.format(self.attacker_combobox.currentText(
            ), self.attack_position_combobox.currentText(), self.point_combobox.currentText(), self.attack_method_combobox.currentText())
        self.current_label = text
        self.annotation_text.setText('Current Label : '+self.current_label)

    def update_original_text(self):
        if not os.path.isfile(self.out_path):
            with open(self.out_path, mode='w', newline='') as file:
                fieldnames = ["Video_name", "Description"]
                writer = csv.DictWriter(file, fieldnames=fieldnames)

                writer.writeheader()

        with open(self.out_path, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            rows = list(reader)

        video_name_exists = False
        for row in rows:
            if row["Video_name"] == os.path.basename(self.current_video_path):
                self.original_text.setText(
                    'Original Label : '+row["Description"])
                video_name_exists = True
                break

        if not video_name_exists:
            self.original_text.setText('Original Label : '+'NO Annotation')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VolleyballLabel()
    window.show()
    sys.exit(app.exec_())
