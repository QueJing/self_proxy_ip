# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 14:46:27 2019

@author: QueJing
"""

# 数据库相关参数
REDIS_HOST = "127.0.0.1"
REDIS_PORT = 6379
REDIS_PASS = None


# 网页数据存储键名称
WEB_DATA_KEY = "web_raw_data"

# 原始IP地址键名称
ORIGINAL_IP_ADDR = "original_ip_addr"

# 检测可用的IP地址键名称
VERIFIED_IP_ADDR = "verified_ip_addr"

# 最大原始IP量
MAX_ORIGINAL_COUNT = 100

# 最大可用IP量
MAX_VERIFIED_COUNT = 20

# 使用以下网站验证IP可用
VERIFY_WEB_LINK = "https://www.baidu.com"
# VERIFY_WEB_LINK = "https://www.wetryer.com"

# 验证超时时间
VERIFY_TIMEOUT = 100

# 验证IP线程数
VERITY_IP_THREAD_COUNT = 10

# 每次获取页面数量
CRAWLER_PAGE_LIMIT = 1

# 常用user-agent
USER_AGENT = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
        "Opera/9.80 (Windows NT 6.1; U; zh-cn) Presto/2.9.168 Version/11.50",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 2.0.50727; SLCC2; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; Tablet PC 2.0; .NET4.0E)",
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; ) AppleWebKit/534.12 (KHTML, like Gecko) Maxthon/3.0 Safari/534.12",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E)",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.41 Safari/535.1 QQBrowser/6.9.11079.201",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)"
        'MSIE (MSIE 6.0; X11; Linux; i686) Opera 7.23',
        'Opera/9.20 (Macintosh; Intel Mac OS X; U; en)',
        'Opera/9.0 (Macintosh; PPC Mac OS X; U; en)',
        'iTunes/9.0.3 (Macintosh; U; Intel Mac OS X 10_6_2; en-ca)',
        'Mozilla/4.76 [en_jp] (X11; U; SunOS 5.8 sun4u)',
        'iTunes/4.2 (Macintosh; U; PPC Mac OS X 10.2)',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:5.0) Gecko/20100101 Firefox/5.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:9.0) Gecko/20100101 Firefox/9.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:16.0) Gecko/20120813 Firefox/16.0',
        'Mozilla/4.77 [en] (X11; I; IRIX;64 6.5 IP30)',
        'Mozilla/4.8 [en] (X11; U; SunOS; 5.7 sun4u)'
        ]

