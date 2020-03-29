# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 14:46:27 2019

@author: QueJing
"""
import aiohttp
import asyncio
import nest_asyncio
import random

from Database.RedisOperation import RedisOperation
from Config.DefaultConfig import WEB_DATA_KEY, USER_AGENT


nest_asyncio.apply()


class CrawlerPages(object):
    """
    抓取一组链接的页面

    以WEB_DATA_KEY为key，以url为属性存储到redis中

    注意：数据分析操作完成后一定要删除相关数据，否则会一直占用内存
    """
    def __init__(self):
        self._redis = RedisOperation()

    async def getPageData(self, url):
        """
        获取某个指定链接的的内容，并保存到数据库中

        参数
        ----------
        url : 字符串 - 指定的链接
        """
        async with aiohttp.ClientSession() as session:
            header = random.choice(USER_AGENT)
            headers = {'User-Agent': header}
            async with session.get(url, headers=headers) as response:
                assert response.status == 200
                data = await response.read()
                self._redis.set(WEB_DATA_KEY, url, data)

    def startCrawler(self, urlList):
        """
        对一组网页地址链接进行爬取，并将结果保存到数据库中

        参数
        ----------
        urlList : 列表 - 待获取的网页地址列表
        """
        try:
            loop = asyncio.get_event_loop()
        except Exception:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        if len(urlList) == 0:
            return
        elif len(urlList) == 1:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(self.getPageData(urlList[0]))
        else:
            tasks = [self.getPageData(url) for url in urlList]
            loop = asyncio.get_event_loop()
            loop.run_until_complete(asyncio.wait(tasks))


'''
以下测试代码的功能是获取urlList中网址的内容，并将相应的内容保存在当前目录下，文件名与地址相同
'''
if __name__ == "__main__":
    urlList = ["http://www.wetryer.com",
               "http://mall.wetryer.com",
               "http://www.66ip.cn"]
    crawlerPages = CrawlerPages()
    crawlerPages.startCrawler(urlList)
    redis = RedisOperation()
    for url in urlList:
        data = redis.get(WEB_DATA_KEY, url)
        redis.delete(WEB_DATA_KEY, url)
        with open(url[7:]+".html", 'w') as file:
            file.write(data)
