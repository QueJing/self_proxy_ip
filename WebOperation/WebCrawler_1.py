# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 14:46:27 2019

@author: QueJing
"""
from WebOperation.WebBaseOperation import WebBaseOperation
from Crawler.CrawlerPages import CrawlerPages
from Config.DefaultConfig import WEB_DATA_KEY
from lxml import etree
import time
import re
from MyLog.MyLog import MyLog


class WebCrawler_1(WebBaseOperation):
    """当前爬取的网站为："""
    webDomain = "http://www.66ip.cn"

    def __init__(self):
        super().__init__()

    def getPageLinks(self):
        """
        从网页中提取页码信息
        用于组合出该网页所有的页面链接地址

        返回值
        --------
        linkLists - 链接的字符串列表
        """
        maxPage = 1
        linkLists = []
        crawler = CrawlerPages()
        crawler.startCrawler([WebCrawler_1.webDomain])
        rawData = self.redis.get(WEB_DATA_KEY, WebCrawler_1.webDomain)
        self.redis.delete(WEB_DATA_KEY, WebCrawler_1.webDomain)
        element = etree.HTML(rawData)
        result = element.xpath("//div/div/a/text()")
        for pageLink in result:
            try:
                temp = int(pageLink)
                if temp > maxPage:
                    maxPage = temp
                if maxPage > 30:
                    break;
            except Exception:
                continue
        for i in range(1, maxPage):
            linkLists.append(WebCrawler_1.webDomain+"/"+str(i)+".html")
        return linkLists

    def decodeIpAddr(self, redis):
        """
        从每个页面中提取IP相关信息并保存
        """
        while True:
            yield 0
            MyLog.log(WebCrawler_1.webDomain+" decoding...")
            linkList = redis.getAllField(WEB_DATA_KEY)
            for link in linkList:
                link = link.decode()
                '''根据原始数据中，属性字符串内是否包含webDomain判断当前网页原始数据是否可以被本对象解析'''
                if link.find(WebCrawler_1.webDomain) == -1:
                    continue
                rawData = redis.get(WEB_DATA_KEY, link)
                redis.delete(WEB_DATA_KEY, link)
                element = etree.HTML(rawData)
                table = element.xpath("//table/tr/td/text()")
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
                    i += 1
                    if i >= tableLen:
                        continue
                    ipLocation = str(table[i])
                    i += 1
                    if i >= tableLen:
                        continue
                    ipType = str(table[i])
                    getTime = time.strftime("%Y-%m-%d %H:%M:%S",
                                            time.localtime())
                    ip = ipAddr[0]+":"+ipPort[0]
                    self.saveIpToDatabase(ip, ipLocation, ipType, getTime)
                    i += 1
            MyLog.log(WebCrawler_1.webDomain+" decode complete")


if __name__ == "__main__":
    webCrawler_1 = WebCrawler_1()
    webCrawler_1.startWebCrawler()
