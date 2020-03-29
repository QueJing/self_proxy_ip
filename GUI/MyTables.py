# -*- coding: utf-8 -*-
"""
Created on Sun Dec 29 16:49:34 2019

@author: QueJing
"""
from GUI.MyTable import MyTable, PageSwitchView
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtCore import Qt
import sys
from PyQt5.QtWidgets import QApplication


class MyTables(QWidget):
    """
    定义一个表格空间，将表格和翻页功能整合到一个控件中
    """

    def __init__(self):
        super().__init__()
        self.myTable = MyTable()
        self.pageSwitchView = PageSwitchView(self.myTable)
        self.myTable.setDataChangedNotifiedFunc(self.pageSwitchView.notifyDataChange)
        self.myTable.setData([])
        self.myTable.showData(1)

        self.__mInit()

    def __mInit(self):
        vLayout = QVBoxLayout()

        vLayout.addWidget(self.myTable, 0, Qt.AlignCenter)
        vLayout.addWidget(self.pageSwitchView, 1, Qt.AlignCenter)

        self.setFixedSize(610, 450)
        self.setLayout(vLayout)

    def setData(self, data):
        """
        设置待显示的数据

        参数
        ----------
        data : 字符串列表 - 列表格式必须与表头格式相同
        """
        self.myTable.setData(data)
        self.myTable.showData(-1)

    def getSelectIpAddr(self):
        """
        获取当前选中的IP地址

        返回值
        ----------
        字符串：选中的IP地址，格式为"IP:Port"，例如"123.45.67.89:1024"
        """
        return self.myTable.getSelectIpAddr()


'''
以下测试代码显示一个带有翻页功能的空表格
'''
if __name__ == "__main__":
    app = QApplication(sys.argv)
    myTables = MyTables()
    myTables.show()

    sys.exit(app.exec_())
