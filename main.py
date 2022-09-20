#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File  : main.py
# @Author: Yxd
# @Date  : 2022/9/20
import sys

from PyQt5.QtCore import QFileInfo
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QApplication
import gui
import ctypes

# windows主图
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")

app = QApplication(sys.argv)


class MyWindows(gui.Ui_MainWindow, QMainWindow):
    def __init__(self):
        super(MyWindows, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("我的应用")
        root = QFileInfo(__file__).absolutePath()
        self.setWindowIcon(QIcon(root + "/images/logo.ico"))
        self.pushButton.clicked.connect(self.signal)

    def signal(self):
        username = self.lineEdit.text()
        print(username)


if __name__ == "__main__":
    my_windows = MyWindows()  # 实例化对象
    my_windows.show()  # 显示窗口
    sys.exit(app.exec_())
