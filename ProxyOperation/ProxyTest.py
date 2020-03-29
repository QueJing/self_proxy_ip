# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 14:15:11 2019

@author: QueJing
"""
import threading
import time
import requests
import random
from Database.RedisOperation import RedisOperation
from Config.DefaultConfig import ORIGINAL_IP_ADDR
from Config.DefaultConfig import VERIFIED_IP_ADDR
from Config.DefaultConfig import MAX_VERIFIED_COUNT, VERITY_IP_THREAD_COUNT, VERIFY_WEB_LINK
from Config.DefaultConfig import USER_AGENT
from MyLog.MyLog import MyLog


class ProxyTest(threading.Thread):

    """
    整个测试过程是：创建VERITY_IP_THREAD_COUNT个SingleIpAddrTestThread线程，每个线程测试一个代理IP
    """
    def __init__(self):
        super().__init__()
        self.exitThreadMark = False
        self.redis = RedisOperation()
        self.singleIpAddrTestThreads = []
        for i in range(VERITY_IP_THREAD_COUNT):
            tempSingleIpAddrTestThread = SingleIpAddrTestThread(self.redis)
            self.singleIpAddrTestThreads.append(tempSingleIpAddrTestThread)

    def exitThread(self):
        """
        退出线程
        """
        SingleIpAddrTestThread.stopSingleIpAddrTestThread()
        self.exitThreadMark = True
        for tempThread in self.singleIpAddrTestThreads:
            tempThread.join()
        self.join()

    def run(self):
        MyLog.log("ip验证线程开始！！")
        for tempSingleTestThread in self.singleIpAddrTestThreads:
            tempSingleTestThread.start()
        while not self.exitThreadMark:

            originalIpAddrs = self.redis.getAllField(ORIGINAL_IP_ADDR)
            originalLength = len(originalIpAddrs)
            '''如果没有得到IP地址，则等待10秒后再次去获取'''
            if originalLength == 0:
                MyLog.log("原始IP为空，10秒后尝试！")
                time.sleep(10)
                continue

            '''遍历所有IP地址，并进行测试'''
            for ipAddr in originalIpAddrs:
                if self.exitThreadMark:
                    break
                ipAddr = ipAddr.decode()
                '''如果已检测的IP地址达到最大值，则等待3秒后再检测'''
                verifiedLength = self.redis.getCount(VERIFIED_IP_ADDR)
                if verifiedLength >= MAX_VERIFIED_COUNT:
                    time.sleep(10)
                    MyLog.log("有效IP存储满，10秒后尝试！")
                    continue

                while not self.exitThreadMark:
                    '''遍历所有的测试线程，看看是否有空闲的线程可以对当前代理IP进行测试，直到找到有线程测试该代理IP之后才退出'''
                    for tempSingleIpAddrTestThread in self.singleIpAddrTestThreads:
                        if tempSingleIpAddrTestThread.setIpAddr(ipAddr):
                            MyLog.log("测试ip：" + ipAddr)
                            ipAddr = None
                            break
                    if ipAddr is None:
                        break
                    time.sleep(1)

        for tempSingleIpAddrTestThread in self.singleIpAddrTestThreads:
            tempSingleIpAddrTestThread.join()
        MyLog.log("ip验证线程结束！！")


class SingleIpAddrTestThread(threading.Thread):
    """
    一个IP代理测试基本过程是：得到一个待测试代理IP，并将这个IP从
    ORIGINAL_IP_ADDR中删除；然后测试这个IP地址是否可用（测试方法见下面的代码）；
    如果可用，则转存到VERITY_IP_ADDR中，最后等待下一个待测试代理IP。
    """

    __stopMark = False

    @staticmethod
    def stopSingleIpAddrTestThread():
        """
        停止所有的SingleIpAddrTestThread线程
        """
        SingleIpAddrTestThread.__stopMark = True

    def __init__(self, redis):
        super().__init__()
        self.ipAddr = None
        self.redis = redis
        self.threadLock = threading.Lock()

    def setIpAddr(self, ipAddr):
        """
        设置要测试的一个代理IP

        参数
        ----------
        ipAddr : 字符串 - 待测试的代理IP字符串，格式为"IP:port"，例如： "123.45.6.7:8888"

        返回值
        -------
        bool True表示设置成功，该线程即将对该代理IP进行测试；False表示设置失败，该线程正在进行其他代理IP的测试。
        """
        isLocked = self.threadLock.locked()
        if isLocked:
            return False

        self.threadLock.acquire()
        self.ipAddr = ipAddr
        return True

    def testMethon_1(self):

        """
        对VERIFY_WEB_LINK采用代理IP进行访问，如果能够获取到数据，表示代理IP有效，否则代理IP无效。

        返回值
        -------
        bool True表示代理IP有效；False表示代理IP无效。

        """
        httpProxy = "http://" + self.ipAddr
        httpsProxy = "https://" + self.ipAddr
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
                MyLog.log(self.ipAddr+"初次验证有效")
                return True
            else:
                MyLog.log(self.ipAddr+"验证无效")
                return False

        except Exception:
            MyLog.log(self.ipAddr+"验证无效"+", 验证异常!")
            return False

    def run(self):
        MyLog.log("single ip addr test start!")

        while not SingleIpAddrTestThread.__stopMark:
            if self.ipAddr is None:
                time.sleep(1)
                continue
            '''开始测试IP地址的可用性'''
            if self.testMethon_1():
                '''地址可用，转存到VERITIED_IP_ADDR中'''
                proxyData = self.redis.get(ORIGINAL_IP_ADDR, self.ipAddr)
                self.redis.set(VERIFIED_IP_ADDR, self.ipAddr, proxyData)
            '''数据测试完成后从数据库中删除'''
            self.redis.delete(ORIGINAL_IP_ADDR, self.ipAddr)

            self.ipAddr = None
            self.threadLock.release()

        MyLog.log("single ip addr test exit!")


'''
以下测试代码的主要开启一个IP代理有效性测试线程

当输入“exit”命令时，退出上面所说的线程
'''
if __name__ == "__main__":
    proxyTest = ProxyTest()
    proxyTest.start()

    while True:
        cmd = input("请输入命令：")
        if cmd == "exit":
            print("设置退出线程")
            proxyTest.exitThread()
            proxyTest.join()
            break
        else:
            MyLog.log("无效命令")
    print("退出线程完成")

