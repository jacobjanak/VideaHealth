import numpy as np
import sys
import cv2

# Qt Wrapper GUI
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
                             QSizePolicy, QDesktopWidget,
                             QLineEdit, QPushButton, QLabel)
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtGui


class ImageController(QWidget):
    image_id = QtCore.pyqtSignal(str)

    def __init__(self, images):
        super().__init__()

        # properties
        self.current = 1
        self.images = images

        # widgets
        self.show_button = None
        self.left_button = None
        self.right_button = None
        self.img_edit = None

        self.init_UI()

    def init_UI(self):
        self.resize(150, 300)
        self.img_edit = QLineEdit()

        self.init_btns()

        hbox = QHBoxLayout()
        hbox.addWidget(self.left_button, stretch=1)
        hbox.addWidget(self.right_button, stretch=1)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox)
        vbox.addWidget(self.img_edit)
        vbox.addWidget(self.show_button)

        self.setLayout(vbox)

        # turn off - and [] buttons and makes window always stay on top
        self.setWindowFlags(self.windowFlags()  # | Qt.CustomizeWindowHint | Qt.WindowStaysOnTopHint
                            # & ~Qt.WindowMinimizeButtonHint
                            & ~Qt.WindowMaximizeButtonHint)
        self.setWindowTitle('Controller')
        self.show()

    def init_btns(self):
        # create buttons
        self.left_button = QPushButton('<', self)
        self.right_button = QPushButton('>', self)
        self.show_button = QPushButton('Show', self)

        # set buttons size to fill out blank spots
        self.left_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.right_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)

        # wire buttons click to react to click
        self.left_button.clicked.connect(self.left_btn_clicked)
        self.right_button.clicked.connect(self.right_btn_clicked)
        self.show_button.clicked.connect(self.show_btn_clicked)

    # Button reactions
    def left_btn_clicked(self):
        if self.current - 1 > 1:
            self.current -= 1
        else:
            self.current = 1

        self.image_id.emit(str(self.current))

    def right_btn_clicked(self):
        if self.current + 1 <= len(self.images):
            self.current += 1

        self.image_id.emit(str(self.current))

    def show_btn_clicked(self):
        user_input = self.img_edit.text()
        if user_input.isdigit() and 1 <= int(user_input) <= len(self.images):
            self.current = int(user_input)

        self.image_id.emit(user_input)
        self.img_edit.clear()

    # user press a key on keyboard
    def keyPressEvent(self, e: QtGui.QKeyEvent) -> None:
        if e.key() == Qt.Key_Return or e.key() == Qt.Key_Enter:
            self.show_btn_clicked()
        else:
            super().keyPressEvent(e)


def show_visualizer(images):
    app = QApplication(sys.argv)
    w = MainWindow(images)
    app.exec_()


def img_cv2_pixmap(cv2_img):
    width = cv2_img.shape[1]
    height = cv2_img.shape[0]
    scale = 0.8

    # resize the opencv image
    screen = QDesktopWidget().screenGeometry()
    width = int(screen.width() * scale)
    height = int(screen.height() * scale)
    img = cv2.resize(cv2_img, (width, height), interpolation=cv2.INTER_AREA)

    # convert opencv image
    img = QImage(img.data, width, height,
                 QImage.Format_RGB888).rgbSwapped()  # convert opencv img to QImage
    return QPixmap.fromImage(img)


class MainWindow(QWidget):
    def __init__(self, images):
        super().__init__()

        # properties
        self.current = 1
        self.images = images

        # widgets
        self.controller = None
        self.image_frame = None
        self.controller_button = None
        self.label = None

        self.init_UI()

    def change_image(self, txt):
        if txt.isdigit():
            # check if image is within range
            if 1 <= int(txt) <= len(self.images):
                self.current = int(txt)
                self.label.setText('img ' + str(int(txt)))
                img = img_cv2_pixmap(self.images[self.current - 1])
                self.image_frame.setPixmap(img)
            else:
                self.label.setText('invalid: {} is out of range. The range is {} - {}.'.format(txt, str(0), str(len(self.images))))
        else:
            self.label.setText('invalid: "' + txt + '" is not a number')

    def init_UI(self):
        self.controller_button = QPushButton('Controller', self)
        self.controller_button.clicked.connect(self.show_controller_window)

        self.label = QLabel()
        hbox = QHBoxLayout()
        hbox.addWidget(self.label)
        hbox.addStretch(2)
        hbox.addWidget(self.controller_button)

        # init image
        img = self.images[self.current - 1]
        img = img_cv2_pixmap(img)  # convert QImage to QPixmap
        self.image_frame = QLabel()
        self.image_frame.setPixmap(img)

        # set image frame fit the window
        self.image_frame.setScaledContents(True)

        # set the label
        self.label.setText('img ' + str(self.current))

        vbox = QVBoxLayout()
        vbox.addWidget(self.image_frame)

        vbox.addLayout(hbox)
        self.setLayout(vbox)

        self.resize(img.size().width(), img.size().height())
        self.center()
        self.setWindowTitle('Visualizer')
        self.show()
        self.show_controller_window()

    def center(self):
        qr = self.frameGeometry()  # get rectangle of our main window
        cp = QDesktopWidget().availableGeometry().center()  # get screen solution of monitor & the center
        qr.moveCenter(cp)  # set center of rectangle to center of screen
        # self.move(qr.topLeft())  # move top left window to top left of qr

    def show_controller_window(self):
        # if image controller is not open
        if self.controller is None:
            self.controller = ImageController(self.images)

            # coordinate of image controller
            x = self.pos().x() + self.frameGeometry().width()  # main window x + main window width
            y = self.pos().y() + self.frameGeometry().height() - self.controller.frameGeometry().y()  # main window y + main window height - controller y
            self.controller.move(x, y)
            self.controller.image_id.connect(self.change_image)
        self.controller.show()

    # window state changed
    def changeEvent(self, e: QtCore.QEvent) -> None:
        if e.type() == QtCore.QEvent.WindowStateChange:
            if e.oldState() and Qt.WindowMinimized:
                self.controller.raise_()  # focus on controller
                pass
                # print('WindowMinimized')
            elif e.oldState() == Qt.WindowNoState or self.windowState() == Qt.WindowMaximized:
                self.controller.raise_()  # focus on controller
                pass
                # print('WindowMaximized')

    # user click X on title bar
    def closeEvent(self, e: QtGui.QCloseEvent) -> None:
        self.controller.close()
        e.accept()
