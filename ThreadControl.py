# -*- coding: utf-8 -*-
"""
Created on Mon Dec 16 22:19:16 2019

@author: QueJing
"""
from threading import Thread, Lock
from ProxyOperation.ProxyTest import ProxyTest
from ProxyOperation.ProxyTestAgain import ProxyTestAgain
from WebOperation.IpGetThread import IpGetThread
from Database.RedisOperation import RedisOperation
from MyLog.MyLog import MyLog


class ThreadControl(Thread):
    """
    定义为Thread的子类，后续需要作为线程运行也可以，作为普通类运行也行

    该类控制整个IP采集的运行和停止，调用run()开始采集，调用exitThread()停止采集
    """
    def __init__(self):
        super().__init__()
        self.exitMark = False
        self.proxyTest = None
        self.proxyTestAgain = None
        self.ipGetThread = None
        self.isRunning = False
        self.threadRuningStatusLock = Lock()

    def exitThread(self):
        self.ipGetThread.exitThread()
        self.proxyTestAgain.exitThread()
        self.proxyTest.exitThread()
        MyLog.log("代理IP采集停止运行")

    def getRunningStatus(self):
        status = False
        with self.threadRuningStatusLock:
            status = self.isRunning
        return status
        
    def run(self):
        with self.threadRuningStatusLock:
            if not self.__dataBaseTest():
                MyLog.log("数据库访问失败！")
                return

        self.isRunning = True
        self.proxyTest = ProxyTest()
        self.proxyTest.start()

        self.proxyTestAgain = ProxyTestAgain()
        self.proxyTestAgain.start()

        self.ipGetThread = IpGetThread()
        self.ipGetThread.start()
        MyLog.log("代理IP采集开始运行")

    def __dataBaseTest(self):
        db = RedisOperation()
        return db.testRedis()


if __name__ == "__main__":
    threadControl = ThreadControl()
    threadControl.start()
    while True:
        cmd = input("请输入命令：")
        if cmd == "exit":
            MyLog.log("开始停止代理IP采集")
            threadControl.exitThread()
            break
        else:
            MyLog.log("无效命令")
