# 1. 描述

本软件希望需要实现以下功能：

- 从免费代理IP网站中获取原始代理IP地址
- 将获取的原始代理IP地址数据存储到数据库中
- 对获取到的原始代理IP地址进行检测，判断其是否可用，如果可用，则存入到数据库中，否则丢弃
- 对可用代理IP地址数据库中的代理IP地址进行检测，判断其是否可用，如果不可用则移除
- 针对Windows操作系统编写可视化操作界面，实现一键获取、设置等功能

# 2. 数据存储

本工程采用redis数据库进行数据存取操作。

采用Hash方式存储，存储格式为(键, 属性, 值)

**键：**

根据代理IP的类型，键的取值为两种：

- 未验证的原始代理IP地址，key值为ORIGINAL_IP_ADDR
- 验证可用的代理IP地址，key值为VERIFIED_IP_ADDR

**属性：**

属性值为代理IP地址，格式为IP:port，例如：123.45.67.89:80

**值：**

值为该代理IP地址对应的对象序列化后的字符串，具体参看Proxy类

# 3. 目录构成

项目的目录结构如下：

        /--
          |--Config/
          |    |--DefaultConfig.py  系统默认配置参数
          |--crawler/
          |    |--CrawlerPages.py 获取网站的全部原始数据，存储到数据库的WEB_DATA_KEY中
          |--Database/
          |    |--ReidsOperation.py  对数据库进行操作
          |--GUI/
          |    |--MainWindow.py  界面主窗口
          |    |--MyButton.py  自定义按键
          |    |--MyButtons.py  界面中的所有按键
          |    |--MyTable.py  自定义表格
          |    |--MyTables.py  界面中的表格
          |    |--SysInfos.py  界面中的提示信息
          |    |--SysInfosRefreshThread.py  更新提示信息的线程
          |    |--TableDataRefreshThread.py  更新表格数据的线程
          |    |--WindowsProxySet.py  Windows系统中设置代理IP
          |--Log/
          |    |--MyLog.py 自定义的Log接口，后续根据需要用于控制Log输出
          |--ProxyOperation/
          |    |--Proxy.py  代理IP对象，包含一个代理IP的相关信息
          |    |--ProxyTest.py 对ORIGINAL_IP_ADDR的IP进行测试，可用则转存到VERIFIED_IP_ADDR中
          |    |--ProxyTestAgain.py 对VERIFIED_IP_ADDR的IP进行测试，不可用则删除
          |--WebOperation/
          |    |--IpGetThread.py  原始代理IP获取线程，调用下方的各网站爬取类爬取原始代理IP
          |    |--WebBaseOperation.py 网站原始数据处理的基类，所有的网站处理都是该类的子类
          |    |--WebCrawler_1.py  第一个爬取的网站（"http://www.66ip.cn"）
          |    |--WebCrawler_2.py  第二个爬取的网站（"https://www.xicidaili.com/nn"）
          |    |--WebCrawler_3.py  第三个爬取的网站（"http://www.89ip.cn"）
          |    |--...   后续需要的话还会继续增加
          |--requirements.txt 所有用到的包
          |--ThreadControl.py 整个爬虫的线程控制类

# 4. 使用

直接运行GUI/MainWindow.py即可