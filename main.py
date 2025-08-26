import os
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from PIL.ImageQt import ImageQt
from PIL import Image
from PyQt6.QtWidgets import (QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout,
                             QListWidget, QFileDialog, QGroupBox, QMessageBox, QProgressBar)
from PyQt6.QtGui import QIcon


class ImageProcessor():
    def __init__(self):
        self.image = None
        self.filename = ''
        self.filepath = ''

    def open(self, filename):
        self.filepath = os.path.join(workdir_path, filename)
        self.filename = filename
        self.image = Image.open(self.filepath)
        if self.image.height < 64 or self.image.width < 64:
            popup = QMessageBox()
            popup.setWindowTitle('Error')
            popup.setText('choose an image with a larger size')
            popup.exec()
            return

        elif self.image.height != self.image.width:
            popup = QMessageBox()
            popup.setWindowTitle('')
            crop_button = popup.addButton('Crop', QMessageBox.ButtonRole.YesRole)
            resize_button = popup.addButton('Resize', QMessageBox.ButtonRole.ApplyRole)
            cancel_button = popup.addButton('Cancel', QMessageBox.ButtonRole.RejectRole)
            popup.setText('Сhoose what to do with the image')
            result = popup.exec()
            clicked = popup.clickedButton()
            if clicked == crop_button:
                if self.image.width > self.image.height:
                    x1, y1 = (self.image.width - self.image.height) // 2, 0
                    x2, y2 = x1 + self.image.height, self.image.height
                    self.image = self.image.crop((x1, y1, x2, y2))
                else:
                    x1, y1 = 0, (self.image.height - self.image.width) // 2
                    x2, y2 = y1 + self.image.width, self.image.width
                    self.image = self.image.crop((x1, y1, x2, y2))

            elif clicked == resize_button:
                if self.image.width < self.image.height:
                    self.image = self.image.resize((self.image.width, self.image.width))
                elif self.image.width > self.image.height:
                    self.image = self.image.resize((self.image.height, self.image.height))

            else:
                print('ffff')
                return

    def show_image(self):
        q_image = ImageQt(self.image)
        pixmap = QPixmap.fromImage(q_image)
        height, width = pic_orig.height(), pic_orig.width()
        pixmap = pixmap.scaled(width, height, Qt.AspectRatioMode.KeepAspectRatio)
        pic_orig.setPixmap(pixmap)


workdir_path = ''
app = QApplication([])
win = QWidget()
win.setFixedSize(700, 500)
win.setWindowTitle('Editor')

layout2 = QVBoxLayout()
layout2_1 = QHBoxLayout()
pic_orig = QLabel('orig')
pic_new = QLabel('new')
layout2_1.addWidget(pic_orig)
layout2_1.addWidget(pic_new)

layout2_2 = QHBoxLayout()
open_button = QPushButton('Open')

fitness_label = QLabel('fitness')
fitness_value = QLabel('0')
progressbar = QProgressBar()
pr_ft_layout = QHBoxLayout()
pr_ft_layout.addWidget(progressbar)
pr_ft_layout.addWidget(fitness_label)
pr_ft_layout.addWidget(fitness_value)

switching_group = QGroupBox()
but_1 = QPushButton()
but_1.setIcon(QIcon('buttons/play.png'))
but_2 = QPushButton()
but_2.setIcon(QIcon('buttons/pause.png'))
but_3 = QPushButton()
but_3.setIcon(QIcon('buttons/stop.png'))
layout_2_2_1 = QHBoxLayout()
layout_2_2_1.addWidget(but_1)
layout_2_2_1.addWidget(but_2)
layout_2_2_1.addWidget(but_3)
switching_group.setLayout(layout_2_2_1)
save_button = QPushButton('Save')

layout2_2.addWidget(open_button)
layout2_2.addWidget(switching_group)
layout2_2.addWidget(save_button)
layout2.addLayout(layout2_1)
layout2.addLayout(pr_ft_layout)
layout2.addLayout(layout2_2)

layout1 = QVBoxLayout()
pictures_label = QLabel('Pictures')
pictures_list = QListWidget()
layout1.addWidget(pictures_label)
layout1.addWidget(pictures_list)

layout_main = QHBoxLayout()
layout_main.addLayout(layout2)
layout_main.addLayout(layout1)
win.setLayout(layout_main)

impr = ImageProcessor()


def open_picture():
    picture_path, _ = QFileDialog.getOpenFileName()
    check = picture_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp'))
    if check:
        impr.open(picture_path)
        impr.show_image()
    else:
        popup = QMessageBox()
        popup.setWindowTitle('Error')
        popup.setText('A file that is not an image has been selected!')
        popup.exec()
        return


def show():
    filename = pictures_list.selectedItems()[0].text()
    impr.open(filename)
    impr.show_image()


open_button.clicked.connect(open_picture)
pictures_list.itemClicked.connect(show)

win.show()
app.exec()
