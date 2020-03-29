# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 10:05:04 2019

@author: QueJing
"""
from WebOperation.WebBaseOperation import WebBaseOperation
from Config.DefaultConfig import WEB_DATA_KEY
from lxml import etree
import time
import re
from MyLog.MyLog import MyLog


class WebCrawler_3(WebBaseOperation):
    webDomain = "http://www.89ip.cn"

    def __init__(self):
        super().__init__()

    def getPageLinks(self):
        """
        从网页中提取页码信息
        用于组合出该网页所有的页面链接地址
        89ip只有6页，所以直接手动输入
        """
        linkLists = ["http://www.89ip.cn/index_1.html",
                     "http://www.89ip.cn/index_2.html",
                     "http://www.89ip.cn/index_3.html",
                     "http://www.89ip.cn/index_4.html",
                     "http://www.89ip.cn/index_5.html",
                     "http://www.89ip.cn/index_6.html"]
        return linkLists

    def decodeIpAddr(self, redis):
        """
        从每个页面中提取IP相关信息并保存
        """
        while True:
            yield 0
            MyLog.log(self.webDomain+" decoding...")
            linkList = redis.getAllField(WEB_DATA_KEY)
            for link in linkList:
                link = link.decode()
                if link.find(self.webDomain) == -1:
                    continue
                rawData = redis.get(WEB_DATA_KEY, link)
                redis.delete(WEB_DATA_KEY, link)
                element = etree.HTML(rawData)
                table = element.xpath("//tbody/tr/td/text()")
                tableLen = len(table)
                i = 0
                while i < tableLen:
                    ipAddr = str(table[i]).strip()
                    ipAddr = re.findall(self.ipAddrRegex, ipAddr)
                    if len(ipAddr) == 0:
                        i += 1
                        continue
                    i += 1
                    if i >= tableLen:
                        continue
                    ipPort = str(table[i]).strip()
                    ipPort = re.findall(self.ipPortRegex, ipPort)
                    if len(ipPort) == 0:
                        continue
                    i += 1
                    if i >= tableLen:
                        continue
                    ipLocation = str(table[i]).strip()
                    '''网站未提供代理类型，默认为普通'''
                    ipType = "普通"
                    getTime = time.strftime("%Y-%m-%d %H:%M:%S",
                                            time.localtime())
                    ip = ipAddr[0]+":"+ipPort[0]
                    self.saveIpToDatabase(ip, ipLocation, ipType, getTime)
                    i += 1
            MyLog.log(self.webDomain+" decode complete")


if __name__ == "__main__":
    webCrawler_3 = WebCrawler_3()
    webCrawler_3.startWebCrawler()
