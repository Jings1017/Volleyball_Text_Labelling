from ui import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget
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


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        with open('./data.json') as f:
            self.data = json.load(f)
        self.setFixedSize(1468, 1014)
        self.add_video_component()
        self.onBindingUI()
        self.combobox_setting()
        self.original_text_label.setWordWrap(True)
        self.current_text_label.setWordWrap(True)
        self.pushButton_switch1.setStyleSheet(
            'background-color: rgb(58, 253, 149);')
        self.pushButton_switch2.setStyleSheet(
            'background-color: rgb(58, 253, 149);')
        self.pushButton_switch3.setStyleSheet(
            'background-color: rgb(58, 253, 149);')

        self.media_content = None
        self.folder_path = ''
        self.current_video_path = None
        self.video_paths = []
        self.current_video_index = 0
        self.save_csv_folder = ''
        self.current_label = ''
        self.out_path = 'label.csv'

    def onBindingUI(self):
        self.pushButton_open_dir.clicked.connect(self.open_dir)
        self.pushButton_save_dir.clicked.connect(self.save_dir)
        self.pushButton_next.clicked.connect(self.load_next_video)
        self.pushButton_prev.clicked.connect(self.load_prev_video)
        self.pushButton_save_text.clicked.connect(self.save_current_data)

        self.pushButton_switch1.clicked.connect(self.switch1_changed)
        self.pushButton_switch2.clicked.connect(self.switch2_changed)
        self.pushButton_switch3.clicked.connect(self.switch3_changed)

        self.pushButton_switch1.clicked.connect(self.on_other_combobox_changed)
        self.pushButton_switch2.clicked.connect(self.on_other_combobox_changed)
        self.pushButton_switch3.clicked.connect(self.on_other_combobox_changed)

        self.media_player.stateChanged.connect(self.mediaStateChanged)
        self.media_player.positionChanged.connect(self.positionChanged)
        self.media_player.durationChanged.connect(self.durationChanged)
        self.media_player.error.connect(self.handleError)

    def combobox_setting(self):
        self.comboBox_score.addItems(['score', 'lose'])
        self.comboBox_state.addItems(['strategy', 'serving'])
        self.comboBox_setter1.addItems(self.data['attacker'])
        self.comboBox_setter2.addItems(self.data['attacker'])
        self.comboBox_attacker.addItems(self.data['attacker'])
        self.comboBox_position_W.addItems(self.data['position'])
        self.comboBox_position_X.addItems(self.data['position'])
        self.comboBox_position_X2.addItems(self.data['position'])
        self.comboBox_position_Y.addItems(self.data['position'])
        self.comboBox_position_Z.addItems(self.data['position'])
        self.comboBox_attack.addItems(self.data['attack_method'])

        self.comboBox_score.currentIndexChanged.connect(
            self.on_score_combobox_changed)
        self.comboBox_state.currentTextChanged.connect(
            self.on_state_combobox_changed)

        self.comboBox_setter1.currentTextChanged.connect(
            self.on_other_combobox_changed)
        self.comboBox_setter2.currentTextChanged.connect(
            self.on_other_combobox_changed)
        self.comboBox_attacker.currentTextChanged.connect(
            self.on_other_combobox_changed)
        self.comboBox_attack.currentTextChanged.connect(
            self.on_other_combobox_changed)
        self.comboBox_position_W.currentTextChanged.connect(
            self.on_other_combobox_changed)
        self.comboBox_position_X.currentTextChanged.connect(
            self.on_other_combobox_changed)
        self.comboBox_position_X2.currentTextChanged.connect(
            self.on_other_combobox_changed)
        self.comboBox_position_Y.currentTextChanged.connect(
            self.on_other_combobox_changed)
        self.comboBox_position_Z.currentTextChanged.connect(
            self.on_other_combobox_changed)

        self.comboBox_position_X.currentTextChanged.connect(
            self.combobox_X_sync
        )

        self.comboBox_position_X2.currentTextChanged.connect(
            self.combobox_X2_sync
        )

    def enable_all_combobox(self):
        self.comboBox_setter1.setDisabled(False)
        self.comboBox_setter2.setDisabled(False)
        self.comboBox_attacker.setDisabled(False)
        self.comboBox_attack.setDisabled(False)
        self.comboBox_position_W.setDisabled(False)
        self.comboBox_position_X.setDisabled(False)
        self.comboBox_position_X2.setDisabled(False)
        self.comboBox_position_Y.setDisabled(False)
        self.comboBox_position_Z.setDisabled(False)

    def disable_all_combobox(self):
        self.comboBox_setter1.setDisabled(True)
        self.comboBox_setter2.setDisabled(True)
        self.comboBox_attacker.setDisabled(True)
        self.comboBox_attack.setDisabled(True)
        self.comboBox_position_W.setDisabled(True)
        self.comboBox_position_X.setDisabled(True)
        self.comboBox_position_X2.setDisabled(True)
        self.comboBox_position_Y.setDisabled(True)
        self.comboBox_position_Z.setDisabled(True)

    def add_video_component(self):
        # add  video media in group
        self.video_layout = QVBoxLayout()
        self.groupBox.setLayout(self.video_layout)

        self.video_widget = QVideoWidget()
        self.video_widget.setFixedSize(960, 540)

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
        self.positionSlider.setRange(0, 100)
        self.positionSlider.setStyleSheet(style)
        self.positionSlider.sliderMoved.connect(self.setPosition)

        self.video_layout.addWidget(self.video_widget)

        self.controlLayout = QHBoxLayout()
        self.controlLayout.addWidget(self.playButton)
        self.controlLayout.addWidget(self.positionSlider)
        self.video_layout.addLayout(self.controlLayout)

    def open_dir(self):
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

    def save_dir(self):
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

    # --- VIDEO SETTING ---
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

    def itemClickedHandler(self, item):

        black_color = QColor(0, 0, 0)
        palette = QPalette()
        palette.setColor(QPalette.WindowText, black_color)
        self.current_text_label.setPalette(palette)

        self.current_video_path = os.path.join(self.folder_path, item.text())

        self.video_title_label.setText(
            os.path.basename(self.current_video_path))
        self.media_content = QMediaContent(
            QUrl.fromLocalFile(self.current_video_path))
        self.media_player.setMedia(self.media_content)
        self.update_original_text()

    def load_next_video(self):
        black_color = QColor(0, 0, 0)
        palette = QPalette()
        palette.setColor(QPalette.WindowText, black_color)
        self.current_text_label.setPalette(palette)

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
        self.current_text_label.setPalette(palette)

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

    def save_current_data(self):

        blue_color = QColor(0, 0, 255)
        palette = QPalette()
        palette.setColor(QPalette.WindowText, blue_color)
        self.current_text_label.setPalette(palette)

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
                self.original_text_label.setText(
                    'Original Label : '+row["Description"])
                video_name_exists = True
                break

        if not video_name_exists:
            self.original_text_label.setText(
                'Original Label : '+'NO Annotation')

    def switch1_changed(self):
        if self.pushButton_switch1.text() == 'ON':
            self.pushButton_switch1.setText('OFF')
            self.pushButton_switch1.setStyleSheet(
                'background-color: rgb(253, 58, 116);')
            self.comboBox_setter1.setDisabled(True)
            self.comboBox_position_W.setDisabled(True)
            self.comboBox_position_X.setDisabled(True)
        else:
            self.pushButton_switch1.setText('ON')
            self.pushButton_switch1.setStyleSheet(
                'background-color: rgb(58, 253, 149);')
            self.comboBox_setter1.setDisabled(False)
            self.comboBox_position_W.setDisabled(False)
            self.comboBox_position_X.setDisabled(False)

    def switch2_changed(self):
        if self.pushButton_switch2.text() == 'ON':
            self.pushButton_switch2.setText('OFF')
            self.pushButton_switch2.setStyleSheet(
                'background-color: rgb(253, 58, 116);')
            self.comboBox_setter2.setDisabled(True)
            self.comboBox_position_X2.setDisabled(True)
            self.comboBox_position_Y.setDisabled(True)
        else:
            self.pushButton_switch2.setText('ON')
            self.pushButton_switch2.setStyleSheet(
                'background-color: rgb(58, 253, 149);')
            self.comboBox_setter2.setDisabled(False)
            self.comboBox_position_X2.setDisabled(False)
            self.comboBox_position_Y.setDisabled(False)

    def switch3_changed(self):
        if self.pushButton_switch3.text() == 'ON':
            self.pushButton_switch3.setText('OFF')
            self.pushButton_switch3.setStyleSheet(
                'background-color: rgb(253, 58, 116);')
            self.comboBox_attacker.setDisabled(True)
            self.comboBox_position_Z.setDisabled(True)
            self.comboBox_attack.setDisabled(True)
        else:
            self.pushButton_switch3.setText('ON')
            self.pushButton_switch3.setStyleSheet(
                'background-color: rgb(58, 253, 149);')
            self.comboBox_attacker.setDisabled(False)
            self.comboBox_position_Z.setDisabled(False)
            self.comboBox_attack.setDisabled(False)

    def on_other_combobox_changed(self, text):
        self.on_state_combobox_changed(self.comboBox_state.currentText())

    def combobox_X_sync(self):
        current_x_index = self.comboBox_position_X.currentIndex()
        self.comboBox_position_X2.setCurrentIndex(current_x_index)

    def combobox_X2_sync(self):
        current_x_index = self.comboBox_position_X2.currentIndex()
        self.comboBox_position_X.setCurrentIndex(current_x_index)

    def on_score_combobox_changed(self):
        if self.comboBox_score.currentText() == 'score':
            self.comboBox_state.clear()
            self.comboBox_state.addItems(['strategy', 'serving'])
        elif self.comboBox_score.currentText() == 'lose':
            self.comboBox_state.clear()
            self.comboBox_state.addItems(
                ['blocking', 'serving error', 'passing mistake', 'attack error'])

    def on_state_combobox_changed(self, text):
        self.enable_all_combobox()
        record_text = ''
        # current_x_index = self.comboBox_position_X.currentIndex()
        # print('the fucking current x index is ', current_x_index)
        # self.comboBox_position_X2.setCurrentIndex(current_x_index)

        if text == 'strategy':
            s_mix = ''

            s1 = f'The {self.comboBox_setter1.currentText()} receives the ball at {self.comboBox_position_W.currentText()} and passes the ball to {self.comboBox_position_X.currentText()}. '

            s2 = f'the {self.comboBox_setter2.currentText()} at {self.comboBox_position_X2.currentText()} sets the ball to {self.comboBox_position_Y.currentText()}, '

            s3 = f'and the {self.comboBox_attacker.currentText()} at {self.comboBox_position_Z.currentText()} gets a point by {self.comboBox_attack.currentText()}.'

            if self.pushButton_switch1.text() == 'ON':
                s_mix += s1
            if self.pushButton_switch2.text() == 'ON':
                s_mix += s2
            if self.pushButton_switch3.text() == 'ON':
                s_mix += s3
            record_text = s_mix

        elif text == 'serving':
            self.disable_all_combobox()
            self.comboBox_position_X.setDisabled(False)
            record_text = f'The server serves the ball to the opponent’s {self.comboBox_position_X.currentText()}, and the oppoent dig outside.'

        elif text == 'blocking':
            s_mix = ''

            s1 = f'The {self.comboBox_setter1.currentText()} receives the ball at {self.comboBox_position_W.currentText()} and passes the ball to {self.comboBox_position_X.currentText()}. '

            s2 = f'the {self.comboBox_setter2.currentText()} at {self.comboBox_position_X2.currentText()} sets the ball to {self.comboBox_position_Y.currentText()}, '

            s3 = f'and the {self.comboBox_attacker.currentText()} at {self.comboBox_position_Z.currentText()} is blocked, leading to a point for the opposing team on a {self.comboBox_attack.currentText()} attack.'

            if self.pushButton_switch1.text() == 'ON':
                s_mix += s1
            if self.pushButton_switch2.text() == 'ON':
                s_mix += s2
            if self.pushButton_switch3.text() == 'ON':
                s_mix += s3
            record_text = s_mix

        elif text == 'serving error':
            self.disable_all_combobox()
            record_text = 'The server loses a point due to a serving error.'

        elif text == 'passing mistake':
            self.comboBox_attacker.setDisabled(True)
            self.comboBox_position_Z.setDisabled(True)
            self.comboBox_attack.setDisabled(True)

            s_mix = ''

            s1 = f'The {self.comboBox_setter1.currentText()} receives the ball at {self.comboBox_position_W.currentText()} and passes the ball to {self.comboBox_position_X.currentText()}. '

            s2 = f'the {self.comboBox_setter2.currentText()} at {self.comboBox_position_X2.currentText()} sets the ball to {self.comboBox_position_Y.currentText()}, '

            s3 = f'and loses a point due to a passing mistake.'

            if self.pushButton_switch1.text() == 'ON':
                s_mix += s1
            if self.pushButton_switch2.text() == 'ON':
                s_mix += s2
            if self.pushButton_switch3.text() == 'ON':
                s_mix += s3
            record_text = s_mix

        elif text == 'attack error':
            s_mix = ''

            s1 = f'The {self.comboBox_setter1.currentText()} receives the ball at {self.comboBox_position_W.currentText()} and passes the ball to {self.comboBox_position_X.currentText()}. '

            s2 = f'the {self.comboBox_setter2.currentText()} at {self.comboBox_position_X2.currentText()} sets the ball to {self.comboBox_position_Y.currentText()}, '

            s3 = f'and the {self.comboBox_attacker.currentText()} at {self.comboBox_position_Z.currentText()} loses a point due to an attack error while executing a {self.comboBox_attack.currentText()} attack.'

            if self.pushButton_switch1.text() == 'ON':
                s_mix += s1
            if self.pushButton_switch2.text() == 'ON':
                s_mix += s2
            if self.pushButton_switch3.text() == 'ON':
                s_mix += s3
            record_text = s_mix

        self.current_label = record_text
        self.current_text_label.setText(
            'Current label : ' + self.current_label)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
