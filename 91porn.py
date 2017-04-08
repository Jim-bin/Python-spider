# -*- coding: utf-8 -*-


import requests, re, random, time, os, csv
from bs4 import BeautifulSoup as bs
from parsel import Selector

headers = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'Accept-Encoding':'gzip, deflate, sdch',
'Accept-Language':'zh-CN,zh;q=0.8',
'Cache-Control':'max-age=0',
'Connection':'keep-alive',
'DNT':'1',
'Host':'email.91dizhi.at.gmail.com.8h9.space',
'Upgrade-Insecure-Requests':'1',
'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

def download_urls(url):
    r = requests.get(url, headers=headers, timeout=30)
    r.encoding = 'utf-8'
    html = r.text
    obj = bs(html, 'html.parser')
    lists = obj.find_all('div', {'class': re.compile('imagechannel.*?')})
    for i in lists:
        try:
            a = i.find('a')
            video_url = a.attrs['href']
            img_url = a.find('img').attrs['src']
            title = a.find('img').attrs['title']
            print(video_url, img_url, title)

            with open('91porn_all.csv', 'a', newline='', encoding='utf_8_sig') as csvfile:
                ww = csv.writer(csvfile, dialect='excel')
                ww.writerow([title, img_url, video_url])
        except:
            continue

def crawl_urls(n):
    for i in range(1,n+1):
        url = 'http://email.91dizhi.at.gmail.com.8h9.space/v.php?category=mf&viewtype=basic&page=' + str(i)
        try:    # 尝试三次，如果3次请求仍然不能成功，则跳过该页，继续爬取下一页
            download_urls(url)
        except:
            try:
                download_urls(url)
            except:
                try:
                    download_urls(url)
                except:
                    continue
    time.sleep(0.001)

n = 3526 # 总页数
crawl_urls(n)
