# -*- coding: utf-8 -*-
"""
Created on Sun Dec 15 20:35:17 2019

@author: QueJing
"""
from threading import Thread
import time

from WebOperation.WebCrawler_1 import WebCrawler_1
from WebOperation.WebCrawler_2 import WebCrawler_2
from WebOperation.WebCrawler_3 import WebCrawler_3
from WebOperation.WebBaseOperation import WebBaseOperation

from MyLog.MyLog import MyLog


class IpGetThread(Thread):
    """
    获取原始代理IP线程，整合所有已知代理IP网站
    """
    def __init__(self):
        super().__init__()
        self.exitThreadMark = False
        temp1 = WebCrawler_1()
        temp2 = WebCrawler_2()
        temp3 = WebCrawler_3()
        self.webOperations = [temp2, temp1, temp3]
    
    def exitThread(self):
        WebBaseOperation.stopWebOperation()
        self.exitThreadMark = True
        self.join()
    
    def run(self):
        MyLog.log("获取IP线程开始")
        length = len(self.webOperations)
        webPosition = -1
        while not self.exitThreadMark:
            webPosition += 1
            MyLog.log("对第"+str(webPosition)+"个网页进行处理")
            webPosition = webPosition % length
            tempWeb = self.webOperations[webPosition]
            tempWeb.startWebCrawler()
        MyLog.log("获取IP线程结束")


'''
以下测试代码的功能是开启原始代理IP获取线程，等待两秒钟后停止该线程。
'''
if __name__ == "__main__":
    ipGetThread = IpGetThread()
    ipGetThread.start()
    time.sleep(2)
    print("设置退出线程")
    ipGetThread.exitThread()
    ipGetThread.join()
    print("退出线程完成")