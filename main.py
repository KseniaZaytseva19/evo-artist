import os
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QTimer
from PIL.ImageQt import ImageQt
from PIL import Image
from PyQt6.QtWidgets import (QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout,
                             QListWidget, QFileDialog, QGroupBox, QMessageBox, QProgressBar)
from PyQt6.QtGui import QIcon
from evoforge import Forge, Algorithm
import threading


class ImageProcessor():
    def __init__(self):
        self.image_orig = None
        self.image_new = None
        self.filename = ''
        self.filepath = ''
        self.forge = Forge(algorithm=Algorithm.MOSAIC)
        self.thread = None

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

        self.image_orig = image

        if self.image_orig.height != self.image_orig.width:
            popup = QMessageBox()
            popup.setWindowTitle('')
            crop_button = popup.addButton('Crop', QMessageBox.ButtonRole.YesRole)
            resize_button = popup.addButton('Resize', QMessageBox.ButtonRole.ApplyRole)
            popup.addButton('Cancel', QMessageBox.ButtonRole.RejectRole)
            popup.setText('Сhoose what to do with the image')
            popup.exec()
            clicked = popup.clickedButton()
            if clicked == crop_button:
                if self.image_orig.width > self.image_orig.height:
                    x1, y1 = (self.image_orig.width - self.image_orig.height) // 2, 0
                    x2, y2 = x1 + self.image_orig.height, self.image_orig.height
                    self.image_orig = self.image_orig.crop((x1, y1, x2, y2))
                else:
                    x1, y1 = 0, (self.image_orig.height - self.image_orig.width) // 2
                    x2, y2 = self.image_orig.width, y1 + self.image_orig.width
                    self.image_orig = self.image_orig.crop((x1, y1, x2, y2))

            elif clicked == resize_button:
                if self.image_orig.width < self.image_orig.height:
                    self.image_orig = self.image_orig.resize((self.image_orig.width, self.image_orig.width))
                elif self.image_orig.width > self.image_orig.height:
                    self.image_orig = self.image_orig.resize((self.image_orig.height, self.image_orig.height))

            else:
                return
        self.forge.open_image(self.image_orig.resize((512, 512)))
        self.forge.reset_algorithm()
        self.thread = threading.Thread(target=self.forge.loop, daemon=True)
        self.thread.start()

    def show_image(self):
        q_image = ImageQt(self.image_orig)
        pixmap = QPixmap.fromImage(q_image)
        height, width = pic_orig.height(), pic_orig.width()
        pixmap = pixmap.scaled(width, height, Qt.AspectRatioMode.KeepAspectRatio)
        pic_orig.setPixmap(pixmap)

    def show_result(self, image):
        self.image_new = image
        q_image = ImageQt(self.image_new)
        pixmap = QPixmap.fromImage(q_image)
        height, width = pic_new.height(), pic_new.width()
        pixmap = pixmap.scaled(width, height, Qt.AspectRatioMode.KeepAspectRatio)
        pic_new.setPixmap(pixmap)

condition = 0
workdir_path = ''
app = QApplication([])
win = QWidget()
win.setFixedSize(1400, 600)
win.setWindowTitle('Editor')
timer = QTimer()


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
play_button = QPushButton()
play_button.setIcon(QIcon('images/play.png'))
play_button.setFixedSize(100, 50)
pause_button = QPushButton()
pause_button.setIcon(QIcon('images/pause.png'))
pause_button.setFixedSize(100, 50)
but_3 = QPushButton()
but_3.setIcon(QIcon('images/stop.png'))
but_3.setFixedSize(100, 50)
layout_2_2_1 = QHBoxLayout()
layout_2_2_1.addWidget(play_button)
layout_2_2_1.addWidget(pause_button)
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


def pause():
    global condition
    if condition == 1:
        impr.forge.pause()
        condition = 2
    else:
        return


def play():
    global condition
    if condition == 0:
        impr.forge.run()
        condition = 1
    elif condition == 2:
        impr.forge.unpause()
        condition = 1
    else:
        return

def save():
    print(impr.forge.get_best_fit())

def update_image():
    if condition == 1:
        image = impr.forge.get_best()
        if image:
            impr.show_result(image)

            fitness = 'fitness: ' +  str(round(impr.forge.get_best_fit(), 2))
            fitness_label.setText(fitness)


open_button.clicked.connect(open_picture)
pictures_list.itemClicked.connect(show)
play_button.clicked.connect(play)
pause_button.clicked.connect(pause)
save_button.clicked.connect(save)
timer.timeout.connect(update_image)
timer.start(1000)
win.show()
app.exec()
