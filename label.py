import sys
import os
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QListView, QHBoxLayout, QWidget, QPushButton, QFileDialog, QLabel, QMessageBox, QComboBox
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import QUrl, QStringListModel
from PyQt5.QtGui import QFont, QColor, QPalette
import csv


class VolleyballLabel(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Volleyball Text Labelling")
        self.setGeometry(100, 100, 1700, 800)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QHBoxLayout(self.central_widget)

        self.buttons_layout = QVBoxLayout()

        self.load_single_button = QPushButton("Open")
        self.load_single_button.setFixedSize(300, 50)
        self.load_single_button.clicked.connect(self.load_single_video)
        self.buttons_layout.addWidget(self.load_single_button)

        self.load_multiple_button = QPushButton("Open Dir")
        self.load_multiple_button.setFixedSize(300, 50)
        self.load_multiple_button.clicked.connect(self.load_multiple_videos)
        self.buttons_layout.addWidget(self.load_multiple_button)

        self.save_location_button = QPushButton("Save Dir")
        self.save_location_button.setFixedSize(300, 50)
        self.save_location_button.clicked.connect(self.select_save_location)
        self.buttons_layout.addWidget(self.save_location_button)

        self.next_video_button = QPushButton("Next Video")
        self.next_video_button.setFixedSize(300, 50)
        self.next_video_button.clicked.connect(self.load_next_video)
        self.buttons_layout.addWidget(self.next_video_button)

        self.previous_video_button = QPushButton("Previous Video")
        self.previous_video_button.setFixedSize(300, 50)
        self.previous_video_button.clicked.connect(self.load_prev_video)
        self.buttons_layout.addWidget(self.previous_video_button)

        self.video_list_view = QListView()
        self.video_list_view.setFixedSize(300, 500)
        self.buttons_layout.addWidget(self.video_list_view)
        self.model = QtGui.QStandardItemModel()
        self.video_list_view.setModel(self.model)
        self.video_list_view.selectionModel().selectionChanged.connect(
            self.handle_selection_changed
        )

        self.select_button = QPushButton("Select")
        self.select_button.setFixedSize(300, 50)
        self.select_button.clicked.connect(self.handle_select_clicked)
        self.buttons_layout.addWidget(self.select_button)

        self.layout.addLayout(self.buttons_layout)

        # ---------------------------------------------------------

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

        self.center_btn_layout = QHBoxLayout()
        self.video_layout.addLayout(self.center_btn_layout)

        self.play_button = QPushButton("Play")
        self.play_button.clicked.connect(self.play_video)
        self.center_btn_layout.addWidget(self.play_button)

        self.done_button = QPushButton("Done")
        self.done_button.clicked.connect(self.save_current_data)
        self.center_btn_layout.addWidget(self.done_button)

        self.original_layout = QHBoxLayout()
        self.video_layout.addLayout(self.original_layout)

        self.original_label = QLabel('  Original label : ')
        self.original_label.setFont(QFont('Arial', 14))
        self.original_label.setAlignment(QtCore.Qt.AlignLeft)
        self.original_layout.addWidget(self.original_label)

        self.original_text = QLabel('')
        self.original_text.setFont(QFont('Arial', 14))
        self.original_text.setAlignment(QtCore.Qt.AlignLeft)
        self.original_layout.addWidget(self.original_text)

        self.anno_layout = QHBoxLayout()
        self.video_layout.addLayout(self.anno_layout)

        self.annotation_label = QLabel('  Current label : ')
        self.annotation_label.setFont(QFont('Arial', 14))
        self.annotation_label.setAlignment(QtCore.Qt.AlignLeft)
        self.anno_layout.addWidget(self.annotation_label)

        self.annotation_text = QLabel('')
        self.annotation_text.setFont(QFont('Arial', 14))
        self.annotation_text.setAlignment(QtCore.Qt.AlignLeft)
        self.anno_layout.addWidget(self.annotation_text)

        # ------------------------------------------------------------

        self.setting_position_layout = QVBoxLayout()
        self.setting_position_text = QLabel('Setting Position')
        self.setting_position_text.setFont(QFont('Arial', 12))
        self.setting_position_text.setAlignment(QtCore.Qt.AlignCenter)
        self.setting_position_layout.addWidget(self.setting_position_text)

        self.setting_position_combobox = QComboBox()
        self.setting_position_combobox.setFixedSize(250, 50)
        self.setting_position_combobox.addItems(
            ['position 1', 'position 2', 'position 3', 'position 4', 'position 5', 'position 6',
             'position 1 and position 2', 'position 2 and position 3', 'position 3 and position 4',
             'position 4 and position 5', 'position 5 and position 6', 'position 1 and position 6'])
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
        self.attacker_combobox.addItems(
            ['outside hitter', 'opposite', 'middle blocker', 'setter', 'libero'])
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
        self.attack_position_combobox.addItems(
            ['position 1', 'position 2', 'position 3', 'position 4', 'position 5', 'position 6',
             'position 1 and position 2', 'position 2 and position 3', 'position 3 and position 4',
             'position 4 and position 5', 'position 5 and position 6', 'position 1 and position 6'])
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
        self.attack_method_combobox.addItems(
            ['spike', 'A quick', 'B quick', 'C quick', 'D quick', 'back-row spike'])
        self.attack_method_layout.addWidget(self.attack_method_combobox)
        self.attack_method_combobox.activated.connect(
            self.update_annotation_text)

        self.custom_choose_layout = QHBoxLayout()
        self.video_layout.addLayout(self.custom_choose_layout)
        self.custom_choose_layout.addLayout(self.setting_position_layout)
        self.custom_choose_layout.addLayout(self.attacker_layout)
        self.custom_choose_layout.addLayout(self.attack_position_layout)
        self.custom_choose_layout.addLayout(self.point_layout)
        self.custom_choose_layout.addLayout(self.attack_method_layout)

        self.media_content = None
        self.folder_path = ''
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

    def load_single_video(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open Video File", "", "Video Files (*.mov *.mp4 *.avi);;All Files (*)", options=options)
        if file_path:
            self.current_video_path = file_path
            self.model.appendRow(QtGui.QStandardItem(
                str(os.path.basename(self.current_video_path))))
            self.video_list_view.setModel(self.model)
            self.media_content = QMediaContent(
                QUrl.fromLocalFile(self.current_video_path))
            self.media_player.setMedia(self.media_content)
            self.video_title_label.setText(
                os.path.basename(self.current_video_path))

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

            for i in range(len(self.show_video_names)):
                self.model.appendRow(QtGui.QStandardItem(
                    str(self.show_video_names[i])))
            self.video_list_view.setModel(self.model)

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

    def handle_selection_changed(self):
        self.select_button.setEnabled(
            bool(self.video_list_view.selectedIndexes()))

    def handle_select_clicked(self):
        for index in self.video_list_view.selectedIndexes():
            item = self.video_list_view.model().itemFromIndex(index)
            print(item.text())
            self.current_video_path = os.path.join(
                self.folder_path, item.text())
            print(self.current_video_path)
            self.video_title_label.setText(
                os.path.basename(self.current_video_path))
            self.media_content = QMediaContent(
                QUrl.fromLocalFile(self.current_video_path))
            self.media_player.setMedia(self.media_content)

    def update_annotation_text(self):
        text = ''
        if 'and' in self.setting_position_combobox.currentText():
            text = 'The setter sets the ball between {},'.format(
                self.setting_position_combobox.currentText())
        else:
            text = 'The setter sets the ball to {},'.format(
                self.setting_position_combobox.currentText())
        if 'and' in self.attack_position_combobox.currentText():
            text += 'and the {} between {} {} a point by {}.'.format(self.attacker_combobox.currentText(
            ), self.attack_position_combobox.currentText(), self.point_combobox.currentText(), self.attack_method_combobox.currentText())
        else:
            text += 'and the {} from {} {} a point by {}.'.format(self.attacker_combobox.currentText(
            ), self.attack_position_combobox.currentText(), self.point_combobox.currentText(), self.attack_method_combobox.currentText())
        self.current_label = text
        self.annotation_text.setText(self.current_label)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VolleyballLabel()
    window.show()
    sys.exit(app.exec_())
