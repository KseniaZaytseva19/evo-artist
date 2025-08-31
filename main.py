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
        image = Image.open(self.filepath)

        if image.height < 64 or image.width < 64:
            popup = QMessageBox()
            popup.setWindowTitle('Error')
            popup.setText('choose an image with a larger size')
            popup.exec()
            return

        self.image = image

        if self.image.height != self.image.width:
            popup = QMessageBox()
            popup.setWindowTitle('')
            crop_button = popup.addButton('Crop', QMessageBox.ButtonRole.YesRole)
            resize_button = popup.addButton('Resize', QMessageBox.ButtonRole.ApplyRole)
            popup.addButton('Cancel', QMessageBox.ButtonRole.RejectRole)
            popup.setText('Сhoose what to do with the image')
            popup.exec()
            clicked = popup.clickedButton()
            if clicked == crop_button:
                if self.image.width > self.image.height:
                    x1, y1 = (self.image.width - self.image.height) // 2, 0
                    x2, y2 = x1 + self.image.height, self.image.height
                    self.image = self.image.crop((x1, y1, x2, y2))
                else:
                    x1, y1 = 0, (self.image.height - self.image.width) // 2
                    x2, y2 = self.image.width, y1 + self.image.width
                    self.image = self.image.crop((x1, y1, x2, y2))

            elif clicked == resize_button:
                if self.image.width < self.image.height:
                    self.image = self.image.resize((self.image.width, self.image.width))
                elif self.image.width > self.image.height:
                    self.image = self.image.resize((self.image.height, self.image.height))

            else:
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
win.setFixedSize(1400, 600)
win.setWindowTitle('Editor')

group_funct = QGroupBox()
group_funct.setFixedWidth(200)
layout2 = QVBoxLayout()
layout2_1 = QHBoxLayout()
pic_orig = QLabel('orig')
pic_new = QLabel('new')
pic_orig.setFixedSize(400, 400)
pic_new.setFixedSize(400, 400)
layout2_1.addWidget(pic_orig)
layout2_1.addWidget(pic_new)

o_image = ImageQt('images/placeHolder.png')
pixmap = QPixmap.fromImage(o_image)
height, width = pic_orig.height(), pic_orig.width()
pixmap = pixmap.scaled(width, height, Qt.AspectRatioMode.KeepAspectRatio)
pic_orig.setPixmap(pixmap)

n_image = ImageQt('images/placeHolder.png')
pixmap = QPixmap.fromImage(n_image)
height, width = pic_new.height(), pic_new.width()
pixmap = pixmap.scaled(width, height, Qt.AspectRatioMode.KeepAspectRatio)
pic_new.setPixmap(pixmap)

progressbar = QProgressBar()

layout2_2 = QHBoxLayout()
open_button = QPushButton('Open')
open_button.setFixedSize(150, 50)
save_button = QPushButton('Save')
save_button.setFixedSize(150, 50)

switching_group = QGroupBox()
switching_group.setFixedSize(400, 75)
but_1 = QPushButton()
but_1.setIcon(QIcon('images/play.png'))
but_1.setFixedSize(100, 50)
but_2 = QPushButton()
but_2.setIcon(QIcon('images/pause.png'))
but_2.setFixedSize(100, 50)
but_3 = QPushButton()
but_3.setIcon(QIcon('images/stop.png'))
but_3.setFixedSize(100, 50)
layout_2_2_1 = QHBoxLayout()
layout_2_2_1.addWidget(but_1)
layout_2_2_1.addWidget(but_2)
layout_2_2_1.addWidget(but_3)
switching_group.setLayout(layout_2_2_1)
layout2_2.addWidget(open_button, alignment=Qt.AlignmentFlag.AlignRight)
layout2_2.addWidget(switching_group)
layout2_2.addWidget(save_button, alignment=Qt.AlignmentFlag.AlignLeft)

layout2.addLayout(layout2_1)
layout2.addWidget(progressbar)
layout2.addLayout(layout2_2)

layout3 = QVBoxLayout()
pictures_label = QLabel('Pictures')
pictures_list = QListWidget()
pictures_list.setFixedWidth(200)
fitness_label = QLabel('fitness : 0')
layout3.addWidget(pictures_label)
layout3.addWidget(pictures_list)
layout3.addWidget(fitness_label, alignment=Qt.AlignmentFlag.AlignCenter)

layout_main = QHBoxLayout()
layout_main.addWidget(group_funct)
layout_main.addLayout(layout2)
layout_main.addLayout(layout3)

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
