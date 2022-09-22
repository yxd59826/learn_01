#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File  : main.py
# @Author: Yxd
# @Date  : 2022/9/20
import sys

from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QFileInfo, QDateTime, QTimer
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QDialog
import time
from apscheduler.schedulers.qt import QtScheduler
import gui
import ctypes
import requests_cache
import login

# windows主图
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")
app = QApplication(sys.argv)
showMessage = QMessageBox.question


def goMainWindow():
    my_windows.show()  # 显示窗口
    login_windows.hide()


class MyWindows(gui.Ui_MainWindow, QMainWindow):
    def __init__(self):
        super(MyWindows, self).__init__()
        self.my_ip = None
        self.setupUi(self)
        self.setWindowTitle("我的应用")
        self.setFixedSize(800, 600)
        font = QtGui.QFont()
        font.setWeight(400)
        font.setFamily("微软雅黑")
        self.setFont(font)
        root = QFileInfo(__file__).absolutePath()
        self.setWindowIcon(QIcon(root + "/images/logo.png"))
        self.getSelfIp()
        self.scheduler = QtScheduler()
        self.pushButton.clicked.connect(self.signal)
        self.pushButton_2.clicked.connect(self.getJobs)
        self.pushButton_3.clicked.connect(self.stopJobs)

    def signal(self):
        username = self.lineEdit.text()
        print(self.my_ip)
        self.textBrowser.append("本机对外IP：" + self.my_ip)
        print(username)

    def getJobs(self):
        self.create_jobs()

    def stopJobs(self):
        self.remove_jobs()

    def getSelfIp(self):
        session = requests_cache.CachedSession('ip_request_cache')
        my_ip_response = session.get("http://httpbin.org/ip")
        response = my_ip_response.json()
        self.my_ip = response['origin']

    def job_function(self):
        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        self.textBrowser.append("任务执行中……，时间：" + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))

    def create_jobs(self):
        go_time = self.lineEdit_3.text()
        if go_time:
            try:
                self.textBrowser.append("启动任务")
                self.scheduler.add_job(self.job_function, trigger="interval", seconds=int(go_time), id='my_job_id')
                self.scheduler.start()
            except Exception as rel:
                print("scheduler start error:", rel)
        else:
            QMessageBox.warning(self, "警告", "请输入时间间隔")

    def remove_jobs(self):
        job = self.scheduler.get_job('my_job_id')
        if job:
            self.textBrowser.append("停止任务")
            self.scheduler.remove_job('my_job_id')
        else:
            self.textBrowser.append("没有任务执行")

    def closeEvent(self, event):
        reply = showMessage(self, '警告', "系统将退出，是否确认?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            job = self.scheduler.get_job('my_job_id')
            if job:
                self.scheduler.shutdown()
            event.accept()
        else:
            event.ignore()


class LoginWindows(login.Ui_Dialog, QDialog):
    def __init__(self):
        super(LoginWindows, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("登录")
        root = QFileInfo(__file__).absolutePath()
        self.setWindowIcon(QIcon(root + "/images/logo.png"))
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        self.lineEdit.setPlaceholderText("请输入用户名")
        self.lineEdit_2.setPlaceholderText("请输入密码")
        self.pushButton.clicked.connect(self.login)

    def login(self):
        username = self.lineEdit.text()
        password = self.lineEdit_2.text()
        if username == "admin" and password == "123":
            goMainWindow()
        else:
            QMessageBox.warning(self, "警告", "用户名密码不正确")

    def keyPressEvent(self, event):
        self.login()


if __name__ == "__main__":
    my_windows = MyWindows()
    login_windows = LoginWindows()
    login_windows.show()
    sys.exit(app.exec_())
