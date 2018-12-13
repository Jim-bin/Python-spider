# -*- coding: utf-8 -*-

'''
在以下环境测试通过：
python 2.7.15或者3.7.0
win10或者lubuntu
'''

# 导入模块
import time
import requests, re, random, os
from bs4 import BeautifulSoup

'''
给定页数，爬取每页所有图片的url，通过此url可以打开图片所在的网页
所有url存在一个列表中
'''
def scrapy_img_urls(nums):
    lss = []
    for num in range(1, nums+1):
        url = 'http://www.doutula.com/photo/list/?page=' + str(num)
        html = requests.get(url, headers=headers)
        html.encoding = 'utf-8'

        text = html.text
        bsop = BeautifulSoup(text, 'html.parser')
        ass = bsop.find('div', {'class': 'page-content'}).find('div').findAll('a')
        
        for a in ass:
            # print(a.attrs['href'])
            lss.append(a.attrs['href'])
        time.sleep(1)
    return lss

'''
接收每个图片的url，打开此url，找到图片真实的地址，通过此地址可以下载图片
找到图片真实的url和名字之后调用download_url函数可以下载图片
'''
def download_img_url(url):
    html = requests.get(url, headers=headers)
    html.encoding = 'utf-8'

    text = html.text
    bsop = BeautifulSoup(text, 'html.parser')
    img = bsop.find('div', {'class': 'col-xs-12 col-sm-12 artile_des'})
    img_url = img.find('img').attrs['src']
    img_title = img.find('img').attrs['alt']
    print(img_url + " " + img_title)

    download_img(img_url, img_title)

'''
下载图片，该函数接收两个参数，一个是图片的真实地址，一个是图片的名字
名字中如果有特殊字符则需要处理，不然windows下可能无法保存，处理名字调用format_name函数
打开指定文件夹保存图片，如果没有则创建。
'''
def download_img(img_url, img_title):
    img_title = format_name(img_title)  # 如果图册名字有特殊字符需要处理。不然在windows下保存不了文件夹
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    os.chdir(file_path)

    # 图片保存到本地
    exists = os.path.exists(img_title)
    if not exists:
        img_html = requests.get(img_url, headers=headers, stream=True, timeout=20, verify=True)
        img_html.encoding = 'utf-8'
        with open(img_title + ".gif", 'wb') as f:
            f.write(img_html.content)
            f.close()


def format_name(img_title):
    '''
    对名字进行处理，如果包含下属字符，则直接剔除该字符
    :param img_title:
    :return:
    '''
    for i in ['\\','/',':','*','?','"','<','>','!','|']:
        while i in img_title:
            img_title = img_title.strip().replace(i, '')
    return img_title

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

nums=5
# 图片存储路径，在linux系统下
# file_path = '/home/zhangyb/downloadfiles/pythonpro/biaoqing'
# 图片存储路径，在windows系统下

file_path = 'E:\downloadfiles\pythonpro\biaoqing'
urls = scrapy_img_urls(nums)
for i in urls:
    print(i)
    download_img_url(i)


# download_img_url('http://www.doutula.com/photo/6437987')
# download_img('https://ws1.sinaimg.cn/large/9150e4e5gy1fx94eo4pdwg203q02g0so.gif', u'好想打死你啊')