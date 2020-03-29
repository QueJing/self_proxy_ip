# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 14:46:27 2019

@author: QueJing
"""
import sys
import redis
import threading
from Config.DefaultConfig import REDIS_HOST, REDIS_PORT, REDIS_PASS
from MyLog.MyLog import MyLog


class RedisOperation(object):
    """
    Redis数据库操作类，实现对Redis数据库的增、删、改、查等功能

    该类采用单例模式设计，全局获取到的redis对象都是一个对象
    """

    # 互斥锁，确保Redis对象在同一时间只有一个操作
    __threadLock = threading.Lock()

    # 单例模式对象，所有获取到的redis都是该对象
    __mRedisOperation = None

    # 网页内容的解码方式
    __decodeMode = ["UTF-8", "GB2312", "ISO-8859-1"]

    def __init__(self):
        pool = redis.ConnectionPool(host=REDIS_HOST, password=REDIS_PASS,
                                    port=REDIS_PORT)
        self._conn = redis.Redis(connection_pool=pool)

    def __new__(cls, *args, **kwargs):
        """
        重写该方法，实现单例模式
        """
        if RedisOperation.__mRedisOperation is None:
            with RedisOperation.__threadLock:
                if RedisOperation.__mRedisOperation is None:
                    RedisOperation.__mRedisOperation = object.__new__(cls)
        return RedisOperation.__mRedisOperation

    def get(self, key, field):
        """
        从数据库中获取数据

        参数
        ----------
        key : 字符串 - 待获取数据的key

        field : 字符串 - 待获取数据的field

        返回值
        -------
        data : 字符串 - 获取到的数据

        """
        data = None
        with RedisOperation.__threadLock:
            try:
                data = self._conn.hget(key, field)
            except Exception as e:
                data = None
                MyLog.log(e)
                return data
        # '''
        # 尝试使用不同的方式解码，得到字符串格式
        # '''
        # i = 0
        # while i < len(self.__decodeMode):
        #     try:
        #         data = data.decode(self.__decodeMode[i])
        #         break
        #     except UnicodeDecodeError:
        #         i += 1
        return data

    def set(self, key, field, value):
        """
        往数据库中添加数据

        参数
        ----------
        key : 字符串 - 待添加数据的key

        field : 字符串 - 待添加数据的field

        value : 字符串或者二进制列表 - 待添加的具体数据

        返回值
        -------
        result : True表示添加成功；False表示添加失败
        """

        result = True
        with RedisOperation.__threadLock:
            try:
                result = self._conn.hset(key, field, value)
            except Exception as e:
                result = False
                MyLog.log(e)

        return result

    def delete(self, key, field):
        """
        删除指定的key-field对

        参数
        ----------
        key : 字符串 - 待删除的key

        field : 字符串 - 待删除的field

        返回值
        -------
        result : True表示删除成功；False表示删除失败
        """
        result = 0
        with RedisOperation.__threadLock:
            try:
                result = self._conn.hdel(key, field)
            except Exception as e:
                result = -1
                MyLog.log(e)

        return result

    def isExist(self, key, field):
        """
        判断数据库中指定的key-field是否存在

        参数
        ----------
        key : 字符串 - 待判断的是否存在的key

        field : 字符串 - 待判定的属性

        返回值
        -------
        result : True表示存在；False表示不存在
        """

        result = 0
        with RedisOperation.__threadLock:
            try:
                result = self._conn.hexists(key, field)
            except Exception as e:
                result = -1
                MyLog.log(e)

        return result

    def getCount(self, key):
        """
        获取指定key下，数据的数量（属性的数量）

        参数
        ----------
        key : 字符串 - 待获取数量的key

        返回值
        -------
        result : 整形 - 数量
        """
        result = 0
        with RedisOperation.__threadLock:
            try:
                result = self._conn.hlen(key)
            except Exception as e:
                result = -1
                MyLog.log(e)

        return result

    def clearAll(self, key):
        """
        清楚指定key下的所有数据

        参数
        ----------
        key : 字符串 - 待清除属性的key值

        返回值
        -------
        result : True 清除成功；False清除失败
        """
        result = 0
        with RedisOperation.__threadLock:
            try:
                result = self._conn.delete(key)
            except Exception as e:
                result = -1
                MyLog.log(e)

        return result

    def getAllField(self, key):
        """
        获取指定key的所有属性值

        参数
        ----------
        key : 字符串 - 待获取属性的key值

        Returns
        -------
        result : 字符串列表 - 所有的属性值
        """

        result = None
        with RedisOperation.__threadLock:
            try:
                result = self._conn.hkeys(key)
            except Exception as e:
                result = None
                MyLog.log(e)

        return result

    def testRedis(self):
        """
        测试数据库是否可以连接

        返回值
        -----
        True 可以连接；False 不能连接
        """
        result = self.set("a", "a", "a")
        if result == -1:
            return False
        result = self.delete("a", "a")
        if result == -1:
            return False
        return True


'''
以下测试内容是往redis数据库中写入、读取、判断是否存在、删除等操作

单步运行代码，配合redis客户端，查看数据库中的数据增删是否符合要求
'''
if __name__ == "__main__":

    db = RedisOperation()
    if not db.testRedis():
        print("database is not avaluable")
        sys.exit(0)

    db.set("xxxx", "a", 1)
    db.set("xxxx", "b", 2)
    print(db.get("xxxx", "a"))
    print(db.get("xxxx", "b"))
    print(db.isExist("xxxx", 'a'))
    print(db.isExist("xxxx", 'c'))
    db.delete("xxxx", "a")
    db.delete("xxxx", "b")
    print(db.get("xxxx", "a"))

    db.set("xxxx", "a", 1)
    db.set("xxxx", "b", 2)
    print("length=%d" % db.getCount("xxxx"))
    db.clearAll("xxxx")
    print("length=%d" % db.getCount("xxxx"))
