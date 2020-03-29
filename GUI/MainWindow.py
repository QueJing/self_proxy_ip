# -*- coding: utf-8 -*-
"""
Created on Sat Dec 21 16:30:28 2019

@author: QueJing
"""

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt
from GUI.MyTables import MyTables
from GUI.MyButtons import MyButtons
from GUI.SysInfos import SysInfos
from GUI.WindowsProxySet import WindowsProxySet
from ThreadControl import ThreadControl
from GUI.TableDataRefreshThread import TableDataRefreshThread
from GUI.SysInfosRefreshThread import SysInfoRefreshThread
from MyLog.MyLog import MyLog
from threading import Thread
import threading


class MainWindow(QWidget):
    __buttonLock = threading.Lock()

    def __init__(self):
        super(MainWindow, self).__init__()
        self.myButtons = MyButtons()
        self.myTables = MyTables()
        self.sysInfos = SysInfos()
        self.threadControl = None
        self.__setLayout()
        self.__setButtonAction()
        self.exitAllThread = None
        self.isStoping = False
        self.isInProxyMode = False

        """开启系统信息显示线程"""
        self.sysInfosRefreshThread = SysInfoRefreshThread(self.sysInfos)
        self.sysInfosRefreshThread.start()
        """开启表格更新线程"""
        self.tableDataRefreshThread = TableDataRefreshThread(self.myTables)
        self.tableDataRefreshThread.start()

    def __setLayout(self):
        """
        设定MainWindow的布局
        """
        hLayout_1 = QHBoxLayout()
        hLayout_1.addWidget(self.myButtons)
        hLayout_1.addWidget(self.sysInfos)
        widget_1 = QWidget()
        widget_1.setLayout(hLayout_1)
        widget_1.setFixedSize(700, 150)

        vLayout = QVBoxLayout()
        vLayout.addWidget(widget_1, 0, Qt.AlignCenter)
        vLayout.addWidget(self.myTables, 1, Qt.AlignCenter)

        self.setLayout(vLayout)
        self.setWindowTitle("Self Proxy v0.1")
        self.setFixedSize(700, 620)

    def __startThread(self):
        """
        开始按键的回调函数
        """
        with MainWindow.__buttonLock:
            self.isStoping = False

            """开启采集线程"""
            if self.threadControl is None:
                self.threadControl = ThreadControl()
                self.threadControl.start()

            """判断采集线程是否开启成功"""
            if not self.threadControl.getRunningStatus():
                self.threadControl = None
                self.myButtons.switchButtonStatus(True)
            else:
                """切换开关状态"""
                self.myButtons.switchButtonStatus(False)

    def __exitThread(self):
        with MainWindow.__buttonLock:
            if not self.isStoping:
                self.isStoping = True
                self.exitAllThread = ExistAllThread(self.__exitThreadFun)
                self.exitAllThread.start()
            else:
                MyLog.log("正在停止中，请勿重复停止！")

    def __exitThreadFun(self):
        """
        退出线程的回调函数
        """
        if self.threadControl is not None:
            self.threadControl.exitThread()
        self.threadControl = None

        """切换开关按键状态"""
        self.myButtons.switchButtonStatus(True)

    def __setIpProxy(self):
        """
        设置代理IP按键的回调函数
        :return:
        """
        with MainWindow.__buttonLock:
            ipString = self.myTables.getSelectIpAddr()
            if sys.platform.find("win") != -1:
                win = WindowsProxySet()
                if self.isInProxyMode:
                    if win.setGlobalProxyIp(""):
                        self.isInProxyMode = False
                        self.myButtons.switchSetProxyButtonText(True)
                else:
                    if ipString is None or ipString is "":
                        MyLog.log("未选中IP")
                    elif win.setGlobalProxyIp(ipString):
                        self.isInProxyMode = True
                        self.myButtons.switchSetProxyButtonText(False)

            elif sys.platform.find("linux") != -1:
                MyLog.log("当前为Linux操作系统，该功能未实现！")
            else:
                MyLog.log("未识别的操作系统！")

    def __setButtonAction(self):
        """设置按键的回调函数"""
        self.myButtons.setFuncs(self.__startThread, self.__exitThread, self.__setIpProxy)

    def closeEvent(self, event):
        self.__exitThread()

        """关闭表格更新线程"""
        if self.tableDataRefreshThread is not None:
            self.tableDataRefreshThread.stopThread()
        self.tableDataRefreshThread = None

        """关闭系统信息显示线程"""
        if self.sysInfosRefreshThread is not None:
            self.sysInfosRefreshThread.stopThread()
        self.sysInfosRefreshThread = None
        event.accept()


class ExistAllThread(Thread):
    def __init__(self, exitFunc):
        super(ExistAllThread, self).__init__()
        self.exitFunc = exitFunc

    def run(self) -> None:
        self.exitFunc()


'''
以下代码是UI的主窗口代码
'''
if __name__ == '__main__':
    app = QApplication(sys.argv)

    mainWindow = MainWindow()

    mainWindow.show()

    sys.exit(app.exec_())
