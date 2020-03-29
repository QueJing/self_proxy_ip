import os
import subprocess
from MyLog.MyLog import MyLog


class WindowsProxySet(object):
    """
    Windows系统中，用于设定系统的代理IP地址
    """
    def setGlobalProxyIp(self, ip=""):

        reg_value = '46,00,00,00,00,00,00,00,01'
        if ip != "":
            reg_value = '46,00,00,00,00,00,00,00,03,00,00,00'
            ipLengthStr = str(hex(len(ip))).replace("0x", "")
            if len(ipLengthStr) == 1:
                ipLengthStr = "0" + ipLengthStr

            reg_value = "%s,%s,00,00,00" % (reg_value, ipLengthStr)

            for i in ip:
                tempValueStr = str(hex(ord(i))).replace("0x", "")
                if len(tempValueStr) == 1:
                    tempValueStr = "0" + tempValueStr
                reg_value = "%s,%s" % (reg_value, tempValueStr)

        settings = 'Windows Registry Editor Version 5.00\n[HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Internet Settings\Connections]\n"DefaultConnectionSettings"=hex:%s' % reg_value

        filePath = '%s/DefaultConnectionSettings.reg' % os.getcwd()
        with open(filePath, 'w') as f:
            f.write(settings)

        (status, resultString) = subprocess.getstatusoutput('reg import "%s"' % filePath)

        if status == 0:
            if ip is "":
                MyLog.log("取消代理IP成功")
            else:
                MyLog.log("设置代理IP成功：" + ip)
            return True
        else:
            if ip is "":
                MyLog.log("取消代理IP失败: %d - %s" % (status, resultString))
            else:
                MyLog.log("设置代理IP失败: %d - %s" % (status, resultString))
            return False


if __name__ == "__main__":
    temp = WindowsProxySet()
    # temp.setGlobalProxyIp("123.45.67.89:1234")
    temp.setGlobalProxyIp("")
