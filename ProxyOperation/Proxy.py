# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 14:46:27 2019

@author: QueJing
"""
import pickle


class Proxy(object):
    """
    存储代理IP的相关信息，包括以下信息：
    ipAddr-IP地址，格式：IP:port
    location-IP地理位置，格式：国家/地区
    ipType-IP类型，透明/匿名/高匿等
    catchTime-获取该IP时间，格式yyyy-MM-dd ss:mm:ss
    """
    def __init__(self, ipAddr, location="", ipType="", catchTime=""):
        self.ipAddr = ipAddr
        self.location = location
        self.ipType = ipType
        self.catchTime = catchTime

    @staticmethod
    def dumpProxy(proxy):
        """
        将代理对象序列化为字节数据，用于存储到数据库中

        参数
        ----------
        proxy : Proxy对象 - 待序列化的代理对象

        返回值
        -------
        s : 对象序列化后的字节数据，可存储于数据库或文件中
        """
        s = pickle.dumps(proxy)
        return s

    @staticmethod
    def loadProxy(s):
        """
        将序列化后的代理对象字节数据反序列化为代理对象

        参数
        ----------
        s : 序列化得到的字节数据

        返回值
        -------
        proxy : 代理对象
        """
        
        proxy = pickle.loads(s)
        return proxy

    def __str__(self):
        """
        自定义对象打印结果
        """
        return self.ipAddr + "," + self.location + "," + self.ipType + "," + self.catchTime

    def getList(self):
        resultList = [self.ipAddr, self.location, self.catchTime, self.ipType]
        return resultList


'''
以下测试内容为新建一个代理对象，将其序列化后再反序列化，得到的两个对象proxy1 和 porxy2打印结果相同
'''
if __name__ == "__main__":
    proxy1 = Proxy("127.2.2.2:345", "中国/北京", "高匿", "12:43")
    print(proxy1)
    s = Proxy.dumpProxy(proxy1)
    proxy2 = Proxy.loadProxy(s)
    print(proxy2)
