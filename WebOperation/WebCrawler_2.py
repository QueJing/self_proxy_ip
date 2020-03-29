# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 14:46:27 2019

@author: QueJing
"""
from WebOperation.WebBaseOperation import WebBaseOperation
from Config.DefaultConfig import WEB_DATA_KEY
from lxml import etree
import time
import re

from MyLog.MyLog import MyLog


class WebCrawler_2(WebBaseOperation):
    """西刺代理"""
    webDomain = "https://www.xicidaili.com/nn"

    def __init__(self):
        super().__init__()

    def getPageLinks(self):
        linkLists = ["https://www.xicidaili.com/nn/1",
                     "https://www.xicidaili.com/nn/2",
                     "https://www.xicidaili.com/nn/3",
                     "https://www.xicidaili.com/nn/4",
                     "https://www.xicidaili.com/nn/5"]
        return linkLists

    def decodeIpAddr(self, redis):
        """
        从每个页面中提取IP相关信息并保存
        """
        while True:
            yield 0
            MyLog.log(self.webDomain+" decoding...")
            linkList = self.redis.getAllField(WEB_DATA_KEY)
            for link in linkList:
                link = link.decode()
                if link.find(self.webDomain) == -1:
                    continue
                rawData = redis.get(WEB_DATA_KEY, link)
                redis.delete(WEB_DATA_KEY, link)
                element = etree.HTML(rawData)
                table = element.xpath("//table/tr/td//text()")
                tableLen = len(table)
                i = 0
                while i < tableLen:
                    ipAddr = str(table[i])
                    ipAddr = re.findall(self.ipAddrRegex, ipAddr)
                    if len(ipAddr) == 0:
                        i += 1
                        continue
                    i += 1
                    if i >= tableLen:
                        continue
                    ipPort = str(table[i])
                    ipPort = re.findall(self.ipPortRegex, ipPort)
                    if len(ipPort) == 0:
                        continue
                    i += 2
                    if i >= tableLen:
                        continue
                    ipLocation = str(table[i])
                    i += 2
                    if i >= tableLen:
                        continue
                    ipType = str(table[i])
                    getTime = time.strftime("%Y-%m-%d %H:%M:%S",
                                            time.localtime())
                    ip = ipAddr[0]+":"+ipPort[0]
                    self.saveIpToDatabase(ip, ipLocation, ipType, getTime)
                    i += 1
            MyLog.log(self.webDomain+" decode complete")


if __name__ == "__main__":
    webCrawler_2 = WebCrawler_2()
    webCrawler_2.startWebCrawler()
