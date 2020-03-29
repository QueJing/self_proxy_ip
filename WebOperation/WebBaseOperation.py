# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 14:46:27 2019

@author: QueJing
"""
from Crawler.CrawlerPages import CrawlerPages
from Database.RedisOperation import RedisOperation
from Config.DefaultConfig import ORIGINAL_IP_ADDR, MAX_ORIGINAL_COUNT, CRAWLER_PAGE_LIMIT

from ProxyOperation.Proxy import Proxy
from MyLog.MyLog import MyLog

import time


class WebBaseOperation(object):
    """
    所有爬取网站类的基类

    针对每个网站都需要编写特定的爬取类，所有的爬取类均需为该类的子类。

    每个爬取类针对网站特点，重写getPageLinks方法和decodeIpAddr方法。

    针对每个网站的爬取类，重写上面的方法后，调用startWebCrawler()方法即可开始对指定网站进行数据爬取
    """

    ''' 当前爬取网站的主页地址，在数据库中作为属性值，判断当前数据库中的数据是否可以被当前对象解析 '''
    webDomain = "http://www.wetryer.com"

    '''IP地址正则表达式'''
    ipAddrRegex = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
    '''端口号正则表达式'''
    ipPortRegex = r"\d{1,5}"

    stopMark = False

    def __init__(self):
        WebBaseOperation.stopMark = False
        self.redis = RedisOperation()

    def getPageLinks(self):
        """
        获取指定网站中所有待爬取的网址列表。该列表根据不同网站可能数量不同，可能只有几个网页，也有可能有上千个网页。

        可根据具体情况和需求，返回期望爬取的链接。

        返回值
        -------
        list 列表 - 所有待爬取的网址链接
        """
        return ["http://www.baidu.com",
                "http://www.wetryer.com",
                "http://mall.wetryer.com"]

    def getAllWebRawData(self, linkList, decodeIp):
        """
        获取所有待爬取链接的原始数据，并将其存储到数据库中，每次爬取的最大数量为CRAWLER_PAGE_LIMIT

        参数
        ----------
        linkList : 字符串列表 - 带爬取链接字符串列表

        decodeIp : generator - 即爬取到原始数据后，用于解析其中的内容的方法
        """
        linkListLen = len(linkList)
        currentLinkPosition = 0
        crawler = CrawlerPages()
        while not WebBaseOperation.stopMark:
            if self.redis.getCount(ORIGINAL_IP_ADDR) >= MAX_ORIGINAL_COUNT:
                MyLog.log("原始IP存储满，爬取暂停，10秒后继续尝试！")
                time.sleep(10)
                continue

            if (currentLinkPosition + CRAWLER_PAGE_LIMIT) > linkListLen:
                subLinkList = linkList[currentLinkPosition:]
                currentLinkPosition = -1
            else:
                subLinkList = linkList[currentLinkPosition:(currentLinkPosition + CRAWLER_PAGE_LIMIT)]
                currentLinkPosition += CRAWLER_PAGE_LIMIT

            crawler.startCrawler(subLinkList)
            decodeIp.send(None)
            if currentLinkPosition == -1:
                break
        decodeIp.close()

    def saveIpToDatabase(self, ip, ipLocation, ipType, getTime):
        """
        将获取到的原始代理IP数据保存到数据库中

        参数
        ----------
        ip :字符串 - 代理IP字符串

        ipLocation :  字符串 - 代理IP地理位置字符串

        ipType : 字符串 - 代理IP类型字符串

        getTime : 字符串 - 代理IP获取的时间字符串
        """
        proxy = Proxy(ip, ipLocation, ipType, getTime)
        self.redis.set(ORIGINAL_IP_ADDR, ip,
                       Proxy.dumpProxy(proxy))

    def decodeIpAddr(self, redis):
        """
        针对每个网站都需要重写该方法，用于从网页原始数据中提取出代理IP地址相关信息

        该方法必须为generator，用于与网页爬取getAllWebRawData构成生产者和消费者模型

        参数
        ----------
        redis : RedisOperation对象 - 用于从数据库中读取原始网址数据提取IP地址信息

        Yields
        ------
        int 无特殊意义
        """
        while True:
            yield 0
            MyLog.log("decoding ...")

    @staticmethod
    def stopWebOperation():
        """
        停止对当前网站的爬取
        """
        WebBaseOperation.stopMark = True

    def startWebCrawler(self):
        """
        开始获取网站所有IP地址操作
        """
        WebBaseOperation.stopMark = False
        decodeIp = self.decodeIpAddr(self.redis)
        decodeIp.send(None)
        linkList = self.getPageLinks()
        self.getAllWebRawData(linkList, decodeIp)


'''
以下测试内容对这个数据获取逻辑进行测试，无特殊意义

数据获取逻辑：1.从getPageLinks中获取待爬链接 --->  2.爬取原始网页内容 ---> 3.解析网页内容 --->重复2和3，直到所有的链接爬取完成 
'''
if __name__ == "__main__":
    webBaseOperation = WebBaseOperation()
    webBaseOperation.startWebCrawler()
