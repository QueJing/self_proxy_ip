# -*- coding: utf-8 -*-
"""
Created on Thu Dec 26 22:23:46 2019

@author: QueJing
"""
import sys
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout


class MyButton(QPushButton):
    """
    自定义一个按键控件
    """

    def __init__(self, text, clickedFunc=None, tipInfo=None):
        super().__init__()
        self.text = text
        self.tipInfo = tipInfo
        self.func = clickedFunc
        self.__mInit()

    def __mInit(self):
        self.setText(self.text)
        if self.tipInfo is not None:
            self.setToolTip(self.tipInfo)
        if self.func is not None:
            self.clicked.connect(self.func)

    def setClickFunc(self, func):
        """
        设置按键的回调函数

        参数
        ----------
        func : 函数名 - 按键按下后的回调函数
        """
        self.func = func
        self.clicked.connect(self.func)


'''
以下代码生成两个按键，点击按键后打印“click”
'''


def myClicked():
    print("click")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = QWidget()
    w.resize(600, 600)
    w.move(300, 300)

    but = MyButton("aaa", clickedFunc=myClicked)
    but1 = MyButton("bbb", clickedFunc=myClicked)

    hLayout = QHBoxLayout()
    hLayout.addWidget(but)
    hLayout.addWidget(but1)

    w.setLayout(hLayout)
    w.show()

    sys.exit(app.exec_())
