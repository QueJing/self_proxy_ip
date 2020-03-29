# -*- coding: utf-8 -*-
"""
Created on Sun Dec 29 20:52:46 2019

@author: QueJing
"""
import sys
from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout, QPlainTextEdit
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from MyLog.MyLog import MyLog


class SysInfos(QWidget):
    """
    自定义一个QWidget，用于显示IP地址和Log信息
    """

    def __init__(self):
        super().__init__()
        self.sysCurrentIpTitle = QLabel("current IP:")
        self.sysCurrentIp = QLabel("")
        self.sysCurrentStatusTitle = QLabel("curent status:")
        self.sysCurrentStatus = QPlainTextEdit()
        self.sysCurrentStatus.setReadOnly(True)
        self.sysCurrentStatusList = []

        self.__mInit()

    def __mInit(self):
        self.setFixedSize(400, 150)

        gridLayout = QGridLayout()

        gridLayout.addWidget(self.sysCurrentIpTitle, 0, 0, alignment=Qt.AlignRight | Qt.AlignTop)
        gridLayout.addWidget(self.sysCurrentIp, 0, 1, alignment=Qt.AlignTop)
        gridLayout.addWidget(self.sysCurrentStatusTitle, 1, 0, alignment=Qt.AlignRight | Qt.AlignTop)
        gridLayout.addWidget(self.sysCurrentStatus, 1, 1, 4, 2, alignment=Qt.AlignTop)

        self.setLayout(gridLayout)

    def addStatusToShow(self, status):
        """
        添加待显示的系统信息

        参数
        ----------
        ipAddr : 字符串 - 待显示的信息
        """
        self.sysCurrentStatusList.append(status)
        if len(self.sysCurrentStatusList) > 100:
            self.sysCurrentStatusList = self.sysCurrentStatusList[1:]
        self.sysCurrentStatus.clear()
        for s in self.sysCurrentStatusList:
            self.sysCurrentStatus.appendPlainText(s)

    def addCurrentIpAddr(self, ipAddr):
        self.sysCurrentIp.setText(ipAddr)

'''
以下测试内容显示一个窗口，窗口中显示IP地址和状态信息
'''
if __name__ == "__main__":
    app = QApplication(sys.argv)
    sysInfos = SysInfos()
    sysInfos.show()
    sys.exit(app.exec_())
