# -*- coding: utf-8 -*-
"""
Created on Mon Dec 23 22:06:49 2019

@author: QueJing
"""
import sys
from PyQt5.QtWidgets import (QTableWidget, QTableView, QWidget, QTableWidgetItem,
                             QLabel, QLineEdit)
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout
from GUI.MyButton import MyButton
from PyQt5.QtWidgets import QApplication, QVBoxLayout
from MyLog.MyLog import MyLog


class MyTable(QTableWidget):
    """
    自定义表格
    """
    
    '''
    每页显示的数量
    '''
    listPerPage = 10
   
    def __init__(self):
        super().__init__()
        self.tableHeadLabels = ['IP地址', '位置', '时间', '类型']
        self.__mInit()
        self.data = []
        self.dataLength = 0
        self.maxPage = 1
        self.currentPage = 1
        self.dataChangedNotifiedFunc = None
        self.selectIpAddr = None
        
    def __mInit(self):
        self.setFixedSize(595, 350)
        self.setRowCount(MyTable.listPerPage) 
        self.setColumnCount(len(self.tableHeadLabels))
        self.setHorizontalHeaderLabels(self.tableHeadLabels)

        self.setShowGrid(True)
        self.setEditTriggers(QTableView.NoEditTriggers)
        self.setColumnWidth(0, 180)
        self.setColumnWidth(1, 120)
        self.setColumnWidth(2, 200)
        self.setColumnWidth(3, 70)
        self.setSelectionBehavior(QTableView.SelectRows)
        self.setSelectionMode(QTableView.SingleSelection)
        self.itemSelectionChanged.connect(self.mySelect)

    def mySelect(self):
        """
        点击表格后的回调函数，用于标记选中的IP地址
        """
        index = self.selectedIndexes()
        if len(index) > 0:
            line = index[0].row()
            itemNumber = line + (self.currentPage - 1) * MyTable.listPerPage
            if 0 <= itemNumber < len(self.data):
                tempString = self.data[itemNumber]
                self.selectIpAddr = tempString[0]
                # MyLog.log("选中IP地址为：" + self.selectIpAddr)
            else:
                self.selectIpAddr = None

    def getSelectIpAddr(self):
        """
        获取选中的代理IP地址
        :return: 字符串-返回选中的代理IP地址，格式：IP:Port
        """
        return self.selectIpAddr

    def setData(self, data):
        """
        设置待显示的数据

        参数
        ----------
        data : 字符串列表 - 列表格式必须与表头格式相同
        """
        
        self.data = data
        self.dataLength = len(data)
        self.maxPage = int(self.dataLength/MyTable.listPerPage + 1)
        if self.dataChangedNotifiedFunc is not None:
            self.dataChangedNotifiedFunc()
    
    def setDataChangedNotifiedFunc(self, dataChangedNotifiedFunc):
        """
        设置更新数据后的回调函数，主要是用于更新翻页界面中的数据

        参数
        ----------
        dataChangedNotifiedFunc : 函数名 - 回调函数
        """
        self.dataChangedNotifiedFunc = dataChangedNotifiedFunc

    def showData(self, page):
        """
        显示指定页数的数据

        参数
        ----------
        page : 整数 - 待显示数据的页数
        """
        self.clear()
        if page >= 0:
            self.currentPage = page

        if self.currentPage > self.maxPage:
            self.currentPage = self.maxPage
        elif self.currentPage < 1:
            self.currentPage = 1
        # if page >= 0:
        #     MyLog.log("当前显示第%d页" % self.currentPage)

        i = (self.currentPage - 1) * MyTable.listPerPage
        j = 0
        while ((i+j) < self.dataLength) and (j < MyTable.listPerPage):
            tempData = self.data[i+j]
            k = 0
            for tempStr in tempData:
                tempStr = str(tempStr)
                tempItem = QTableWidgetItem(tempStr)
                tempItem.setTextAlignment(Qt.AlignCenter)
                self.setItem(j, k, tempItem)
                k += 1
            j += 1


class PageSwitchView(QWidget):
    """
    自定义翻页类，实现上一页、下一页切换
    """
    def __init__(self, myTable):
        super().__init__()
        self.myTable = myTable
        self.hLayout = QHBoxLayout()
        self.preButton = MyButton("pre", clickedFunc=self.prePageClicked)
        self.nextButton = MyButton("next", clickedFunc=self.nexPageClicked)
        self.allPageNum = QLabel()
        self.currentPageEdit = QLineEdit()
        
        self.__mInit()
    
    def notifyDataChange(self):
        """
        根据表格中的数据量更新翻页中的数据
        """
        self.allPageNum.setText("/"+str(self.myTable.maxPage))
        self.currentPageEdit.setText(str(self.myTable.currentPage)) 
        
    def prePageClicked(self):
        """
        将表格内容显示切换到上一页
        """
        self.myTable.showData(self.myTable.currentPage - 1)
        self.notifyDataChange()

    def nexPageClicked(self):
        """
        将表格内容显示切换到下一页
        """
        self.myTable.showData(self.myTable.currentPage + 1)
        self.notifyDataChange()
    
    def __mInit(self):
        self.preButton.setFixedWidth(50)
        self.nextButton.setFixedWidth(50)
        self.allPageNum.setFixedWidth(50)
        self.currentPageEdit.setFixedWidth(40)
        
        self.hLayout.addWidget(self.preButton)
        self.hLayout.addWidget(self.currentPageEdit)
        self.hLayout.addWidget(self.allPageNum)
        self.hLayout.addWidget(self.nextButton)
        
        self.currentPageEdit.setAlignment(Qt.AlignCenter)
        self.setLayout(self.hLayout)
        

'''
以下测试代码显示一张表格，将eampleData中的数据显示到表格中
'''    
if __name__ == '__main__':
    exampData = [["123.12.23.4:9999", "China", "2019-12-23 12:52:18", "type-1"],
                 ["123.12.23.5:9999", "China", "2019-12-23 12:52:18", "type-1"],
                 ["123.12.23.6:9999", "China", "2019-12-23 12:52:18", "type-1"],
                 ["123.12.23.7:9999", "China", "2019-12-23 12:52:18", "type-1"],
                 ["123.12.23.8:9999", "China", "2019-12-23 12:52:18", "type-1"]]
    app = QApplication(sys.argv)
    
    w = QWidget()
    w.resize(600, 800)
    w.move(300, 300)
    w.setWindowTitle('Simple')
    
    table = MyTable()
    vLayout = QVBoxLayout()
    vLayout.addWidget(table, 0, Qt.AlignCenter)
    pageSwitchView = PageSwitchView(table)
    vLayout.addWidget(pageSwitchView, 1, Qt.AlignCenter)
    table.setDataChangedNotifiedFunc(pageSwitchView.notifyDataChange)
    w.setLayout(vLayout)
    
    table.setData(exampData)
    table.showData(6)
    
    w.show()
    
    sys.exit(app.exec_())
