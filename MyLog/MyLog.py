# -*- coding: utf-8 -*-
"""
Created on Fri Nov 17 22:12:27 2019

@author: QueJing
"""
import threading


class MyLog:
    """
    自定义Log，调用log方法，实现指定操作
    """

    __threadLock = threading.Lock()
    __sysInfosThread = None

    @staticmethod
    def log(s):
        with MyLog.__threadLock:
            print(s)
            if MyLog.__sysInfosThread is not None:
                MyLog.__sysInfosThread.addNewInfo(s)

    @staticmethod
    def setSysInfosThread(sysInfosThread):
        with MyLog.__threadLock:
            MyLog.__sysInfosThread = sysInfosThread
