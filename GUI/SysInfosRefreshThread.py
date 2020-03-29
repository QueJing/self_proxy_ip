from MyLog.MyLog import MyLog
from PyQt5.QtCore import *
import socket


class SysInfoRefreshThread(QThread):
    """
    该线程用于更新系统信息，通过
    """
    newSystemInfoString = pyqtSignal(str)
    currentHostIpAddr = pyqtSignal(str)

    def __init__(self, sysInfos):
        super(SysInfoRefreshThread, self).__init__()
        self.__stopThreadMark = False
        self.newSystemInfoString.connect(sysInfos.addStatusToShow)
        self.currentHostIpAddr.connect(sysInfos.addCurrentIpAddr)
        self.infoSemaphore = QSemaphore(0)
        self.newInfo = ""
        self.currentIp = None
        MyLog.setSysInfosThread(self)

    def stopThread(self):
        """
        停止更新系统信息线程
        :return:
        """
        self.__stopThreadMark = True
        self.infoSemaphore.release(1)
        self.quit()
        self.wait()
        MyLog.log("系统信息更新线程退出")

    def addNewInfo(self, info):
        """
        外部调用，用于将待显示的信息加入
        :param info: 字符串 - 待显示的信息
        """
        self.newInfo = info
        self.infoSemaphore.release(1)

    def run(self) -> None:
        MyLog.log("系统信息更新线程开启")
        while not self.__stopThreadMark:
            """获取IP地址"""
            hostName = socket.gethostname()
            tempIpAddr = socket.gethostbyname(hostName)
            if self.currentIp is None or tempIpAddr is self.currentIp:
                self.currentIp = tempIpAddr
                self.currentHostIpAddr.emit(self.currentIp)

            """打印信息"""
            self.infoSemaphore.acquire(1)
            if self.newInfo is not None:
                self.newSystemInfoString.emit(self.newInfo)
                self.newInfo = None
