# -*- coding: utf-8 -*-
"""
Created on Thu Dec 26 22:47:49 2019

@author: QueJing
"""
from GUI.MyButton import MyButton
from PyQt5.QtWidgets import QWidget, QVBoxLayout
import sys
from PyQt5.QtWidgets import QApplication


class MyButtons(QWidget):
    """
    自定义一组按键（三个），包括开始、结束和设置代理按键
    """

    def __init__(self):
        super().__init__()
        self.startButton = MyButton("Start")
        self.setProxyButton = MyButton("Set Proxy")
        self.stopButton = MyButton("Stop")
        self.vLayout = QVBoxLayout()

        self.__mInit()

    def __mInit(self):
        self.setFixedSize(200, 150)
        self.stopButton.setEnabled(False)
        self.vLayout.addWidget(self.startButton)
        self.vLayout.addWidget(self.stopButton)
        self.vLayout.addWidget(self.setProxyButton)
        self.setLayout(self.vLayout)

    def setFuncs(self, startFunc=None, stopFunc=None, setProxyFunc=None):
        """
        分别设置这一组按键的回调函数

        参数
        ----------
        startFunc : 函数名 - 开始按键的回调函数

        stopFunc : 函数名 - 结束按键的回调函数

        setProxyFunc : 函数名 - 设置为代理按键的回调函数
        """
        if startFunc is not None:
            self.startButton.setClickFunc(startFunc)
        if stopFunc is not None:
            self.stopButton.setClickFunc(stopFunc)
        if setProxyFunc is not None:
            self.setProxyButton.setClickFunc(setProxyFunc)

    def switchButtonStatus(self, enableStart):
        """
        切换开始和停止按键状态的函数
        :param enableStart: 布尔类型  - True 表示使能开始按键，禁用停止按键；False则表示使能停止按键，禁用开始按键
        """
        if enableStart:
            self.startButton.setEnabled(True)
            self.stopButton.setEnabled(False)
        else:
            self.startButton.setEnabled(False)
            self.stopButton.setEnabled(True)

    def switchSetProxyButtonText(self, isSet):
        """
        设置  设置代理IP 按键的名称
        :param isSet: 布尔型 - True设置为设置代理IP，False设置为重置代理IP
        :return:
        """
        if isSet:
            self.setProxyButton.setText("Set Proxy")
        else:
            self.setProxyButton.setText("Reset Proxy")


def startClick():
    print("set func click")


'''
以下代码显示一组按键（三个）
'''
if __name__ == '__main__':
    app = QApplication(sys.argv)

    myButton = MyButtons()
    myButton.show()

    myButton.setFuncs(startFunc=startClick)

    sys.exit(app.exec_())
