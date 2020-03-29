from Config.DefaultConfig import VERIFIED_IP_ADDR
from Database.RedisOperation import RedisOperation
from MyLog.MyLog import MyLog
import time
from ProxyOperation.Proxy import Proxy
from PyQt5.QtCore import *


class TableDataRefreshThread(QThread):
    """
    表格更新线程，用于更新表格中的数据
    """
    verifiedIpList = pyqtSignal(list)

    def __init__(self, myTables):
        super(TableDataRefreshThread, self).__init__()
        self.__stopThreadMark = False
        self.verifiedIpList.connect(myTables.setData)

    def stopThread(self):
        """
        停止表格更新线程
        """
        self.__stopThreadMark = True
        self.quit()
        self.wait()
        MyLog.log("更新表格线程退出")

    def run(self) -> None:
        redis = RedisOperation()
        MyLog.log("更新表格线程开启")
        while not self.__stopThreadMark:
            ipFinalList = []
            ipAddrList = redis.getAllField(VERIFIED_IP_ADDR)
            for temp in ipAddrList:
                tempData = redis.get(VERIFIED_IP_ADDR, temp)
                tempProxy = Proxy.loadProxy(tempData)
                ipFinalList.append(tempProxy.getList())
            if len(ipFinalList) > 0:
                self.verifiedIpList.emit(ipFinalList)
            time.sleep(5)
