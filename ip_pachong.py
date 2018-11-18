# -*- coding: utf-8 -*-

'''
python 3.7.0
'''

# 导入模块
import time
import requests, re, random, os
from bs4 import BeautifulSoup

def ip_test(ip, url_for_test='https://www.baidu.com', set_timeout=10):
    '''
    检测爬取到的ip地址可否使用，能使用返回True，否则返回False，默认去访问百度测试代理
    :param ip:
    :param url_for_test:
    :param set_timeout:
    :return:
    '''
    try:
        r = requests.get(url_for_test, headers=headers, proxies={'http': ip[0]+':'+ip[1]}, timeout=set_timeout)
        if r.status_code == 200:
            return True
        else:
            return False
    except:
        return False

def scrawl_ip(url, num, url_for_test='https://www.baidu.com'):
    '''
    爬取代理ip地址，代理的url是西祠代理
    :param url:
    :param num:
    :param url_for_test:
    :return:
    '''
    ip_list = []
    for num_page in range(1, num+1):
        url = url + str(num_page)

        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8'
        content = response.text

        pattern = re.compile('<td class="country">.*?alt="Cn" />.*?</td>.*?<td>(.*?)</td>.*?<td>(.*?)</td>', re.S)
        items = re.findall(pattern, content)
        for ip in items:
            if ip_test(ip[1], url_for_test):  # 测试爬取到ip是否可用，测试通过则加入ip_list列表之中
                print('测试通过，IP地址为' + str(ip[0]) + ':' + str(ip[1]))
                ip_list.append(ip[0]+':'+ip[1])
        return ip_list

    time.sleep(5)  # 等待5秒爬取下一页

def get_random_ip():    # 随机获取一个IP
    ind = random.randint(0, len(total_ip)-1)
    return total_ip[ind]


# 爬取代理的url地址，选择的是西祠代理
url_ip = "http://www.xicidaili.com/nt/"

# 设定等待时间
set_timeout = 10

# 爬取代理的页数，2表示爬取2页的ip地址
num = 2

# 代理的使用次数
count_time = 5

# 构造headers
UserAgent_List = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]

headers = {'User-Agent': random.choice(UserAgent_List),
           'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
           'Accept-Encoding': 'gzip',
           }


# 爬取IP代理
total_ip = scrawl_ip(url_ip, num)





