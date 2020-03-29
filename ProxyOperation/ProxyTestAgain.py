# -*- coding: utf-8 -*-
"""
Created on Fri Dec 16 14:15:11 2019

@author: QueJing
"""
from threading import Thread
from Database.RedisOperation import RedisOperation
from Config.DefaultConfig import VERIFIED_IP_ADDR, VERIFY_WEB_LINK
from Config.DefaultConfig import USER_AGENT
import time
import requests
import random
from MyLog.MyLog import MyLog


class ProxyTestAgain(Thread):

    """
    IP代理再次测试：已经确认的IP地址，可能后面会失效，所以需要再次测试，在VERIFIED_IP_ADDR中的IP都是可用的
    基本过程是：从VERIFIED_IP_ADDR中获取一个IP地址（field）；然后测试这个IP地址是否可用（测试方法见下面的代码）；
    如果可用，不变化，如果不可用，删除
    """

    def __init__(self):
        super().__init__()
        self.exitThreadMark = False

    def testMethon1(self, ipAddr):
        """
        验证IP地址是否有效

        参数
        ----------
        ipAddr : 字符串 - 待测试的代理IP字符串，格式为"IP:port"，例如： "123.45.6.7:8888"

        返回值
        -------
        bool True表示代理IP有效；False表示代理IP无效。
        """
        MyLog.log("再次验证ip" + ipAddr)
        httpProxy = "http://"+ipAddr
        httpsProxy = "https://"+ipAddr
        proxies = {
            'http': httpProxy,
            'https': httpsProxy
        }
        try:
            header = random.choice(USER_AGENT)
            headers = {'User-Agent': header}
            html = requests.get(VERIFY_WEB_LINK,
                                headers=headers,
                                proxies=proxies)
            if html.status_code == 200:
                MyLog.log(ipAddr+"再次验证有效")
                return True
            else:
                MyLog.log(ipAddr+"再次验证无效")
                return False
        except Exception:
            MyLog.log(ipAddr+"再次验证无效， 验证异常！")
            return False

    def exitThread(self):
        """
        退出线程
        """
        self.exitThreadMark = True
        self.join()

    def run(self):
        MyLog.log("ip二次确认线程开启！！")
        redis = RedisOperation()
        timeCount = 600
        timeCountLimit = 600 #每隔10分钟进行 二次验证
        while not self.exitThreadMark:
            '''开始计时'''
            time.sleep(1)
            timeCount += 1

            if timeCount < timeCountLimit:
                continue
            MyLog.log("开始本次二次确认")
            timeCount = 0
            ipAddrAgain = redis.getAllField(VERIFIED_IP_ADDR)
            ipAddrAgainLength = len(ipAddrAgain)
            '''遍历所有IP地址，并进行测试'''
            if ipAddrAgainLength > 0:
                for ipAddr in ipAddrAgain:
                    if self.exitThreadMark:
                        break
                    ipAddr = ipAddr.decode()
                    '''开始测试IP地址的可用性'''
                    if not self.testMethon1(ipAddr):
                        '''地址不可用，从VERITIED_IP_ADDR中删除'''
                        redis.delete(VERIFIED_IP_ADDR, ipAddr)
            MyLog.log("本次二次确认完成")
        MyLog.log("ip二次确认线程结束！！")


if __name__ == "__main__":
    proxyTestAgain = ProxyTestAgain()
    proxyTestAgain.start()

    while True:
        cmd = input("请输入命令：")
        if cmd == "exit":
            print("设置退出线程")
            proxyTestAgain.exitThread()
            proxyTestAgain.join()
            break
        else:
            MyLog.log("无效命令")    
    print("退出线程完成")

