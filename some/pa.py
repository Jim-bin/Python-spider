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
from requests import Session

session = Session()


'''
给定页数，爬取每页所有图片的url，通过此url可以打开图片所在的网页
所有url存在一个列表中
'''


def scrapy_img_urls(nums):
    lss = []
    for num in range(1, nums + 1):
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
    for i in ['\\', '/', ':', '*', '?', '"', '<', '>', '!', '|']:
        while i in img_title:
            img_title = img_title.strip().replace(i, '')
    return img_title


def royal(url):
    html = requests.get(url, headers=headers, stream=True, timeout=20, verify=True)
    html.encoding = 'utf-8'
    text = html.text
    bsop = BeautifulSoup(text, 'html.parser')
    timeofissued = bsop.find('meta', {'name':'DC.issued'}).attrs['content'].split('/')[0]
    citation_title = bsop.find('meta', {'name':'citation_title'}).attrs['content']
    citation_journal_title = bsop.find('meta', {'name':'citation_journal_title'}).attrs['content']
    citation_journal_abbrev = bsop.find('meta', {'name':'citation_journal_abbrev'}).attrs['content']
    citation_volume = bsop.find('meta', {'name':'citation_volume'}).attrs['content']
    citation_issue = bsop.find('meta', {'name':'citation_issue'}).attrs['content']
    citation_firstpage = bsop.find('meta', {'name':'citation_firstpage'}).attrs['content']
    citation_lastpage = bsop.find('meta', {'name':'citation_lastpage'}).attrs['content']
    citation_doi = bsop.find('meta', {'name':'citation_doi'}).attrs['content']
    PB = bsop.find('meta', {'name':'DC.publisher'}).attrs['content']
    M3 = citation_doi
    citation_url = 'http://dx.doi.org/' + citation_doi
    citation_abstract = bsop.find('meta', {'name':'citation_abstract'}).attrs['content'].strip()
    SN = bsop.find('div', {'class':'article-nav__issue autopad--h'}).find('a').attrs['href'].split('=')[-1]

    with open(citation_title + ".ris", 'w') as f:
        f.write('TY  - JOUR\n')
        f.write('T1  - ' + citation_title + '\n')
        f.write('Y1  - ' + timeofissued + '\n')
        f.write('SP  - ' + citation_firstpage + '\n')
        f.write('EP  - ' + citation_lastpage + '\n')
        f.write('JF  - ' + citation_journal_title + '\n')
        f.write('JO  - ' + citation_journal_abbrev + '\n')
        f.write('VL  - ' + citation_volume + '\n')
        f.write('RS  - ' + citation_issue + '\n')
        f.write('PB  - ' + PB + '\n')
        f.write('SN  - ' + SN + '\n')
        f.write('DO  - ' + citation_doi + '\n')
        f.write('M3  - ' + M3 + '\n')
        f.write('UR  - ' + citation_url + '\n')
        print(citation_url)
        f.write('N2  - ' + citation_abstract + '\n')
        print(citation_abstract)

        authors = bsop.findAll('span', {'class': 'article__author-link'})
        for author in authors:
            author = author.find('a').text.split(' ')
            author = author[-1] + ', ' + ' '.join(author[:-1])
            f.write('A1  - ' + author + '\n')
        f.write('ER  - ' + '\n')
        f.close()

    # authors = bsop.findAll('span', {'class':'article__author-link'})
    # for author in authors:
    #     author = author.find('a').text.split(' ')
    #     author = author[-1] + ', ' + ' '.join(author[:-1])
    #     with open(author + ".ris", 'w') as f:
    #         f.write('TY  - JOUR')
    #         f.write('T1  - ' + citation_title)
    #         f.write('T1  - ' + authors)
    #         f.close()

    #     print(author)
    # print(timeofissued)





    # print(authors)
    # with open("ro.ris", 'wb') as f:
    #     f.write(html.content)
    #     f.close()


def scawurls(url):

    headers1 = {
        'Accept':'text/html, */*; q=0.01',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'DNT':'1',
        'Host':'pubs.rsc.org',
        'Origin':'https://pubs.rsc.org',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
        'X-NewRelic-ID':'VQYFWF9aDBABV1laBgcFUw ==',
        'X-Requested-With':'XMLHttpRequest'
    }

    data = {
        'searchterm': 'AAEAAAD/////AQAAAAAAAAAMAgAAAGNSU0NwdWJzLmVQbGF0Zm9ybS5TZXJ2aWNlLkRhdGFDb250cmFjdHMsIFZlcnNpb249MjAxOC4wLjU0OS4wLCBDdWx0dXJlPW5ldXRyYWwsIFB1YmxpY0tleVRva2VuPW51bGwFAQAAADlSU0NwdWJzLmVQbGF0Zm9ybS5TZXJ2aWNlLkRhdGFDb250cmFjdHMuU2VhcmNoLlNlYXJjaFRlcm0OAAAAGTxDYXRlZ29yeT5rX19CYWNraW5nRmllbGQcPFN1YkNhdGVnb3J5PmtfX0JhY2tpbmdGaWVsZBw8Q29udGVudFR5cGU + a19fQmFja2luZ0ZpZWxkGjxDcml0ZXJpYXM + a19fQmFja2luZ0ZpZWxkFzxGYWNldHM + a19fQmFja2luZ0ZpZWxkHDxSZXF1ZXN0VGltZT5rX19CYWNraW5nRmllbGQfPEF1dGhvckNyaXRlcmlhPmtfX0JhY2tpbmdGaWVsZCA8UHVibGljYXRpb25EYXRlPmtfX0JhY2tpbmdGaWVsZBk8RXhjbHVkZXM + a19fQmFja2luZ0ZpZWxkFzxTb3VyY2U + a19fQmFja2luZ0ZpZWxkHzxPdXRwdXRTdGFuZGFyZD5rX19CYWNraW5nRmllbGQePFJlc3VsdHNGb3JtYXQ + a19fQmFja2luZ0ZpZWxkHjxEaXNwbGF5Q291bnRzPmtfX0JhY2tpbmdGaWVsZCA8UHJvZHVjdFBhZ2VTaXplPmtfX0JhY2tpbmdGaWVsZAEBAQMDAAQEAwEBAQEBwgFTeXN0ZW0uQ29sbGVjdGlvbnMuR2VuZXJpYy5MaXN0YDFbW1JTQ3B1YnMuZVBsYXRmb3JtLlNlcnZpY2UuRGF0YUNvbnRyYWN0cy5FbnRpdHkuTmFtZVZhbHVlLCBSU0NwdWJzLmVQbGF0Zm9ybS5TZXJ2aWNlLkRhdGFDb250cmFjdHMsIFZlcnNpb249MjAxOC4wLjU0OS4wLCBDdWx0dXJlPW5ldXRyYWwsIFB1YmxpY0tleVRva2VuPW51bGxdXcIBU3lzdGVtLkNvbGxlY3Rpb25zLkdlbmVyaWMuTGlzdGAxW1tSU0NwdWJzLmVQbGF0Zm9ybS5TZXJ2aWNlLkRhdGFDb250cmFjdHMuRW50aXR5Lk5hbWVWYWx1ZSwgUlNDcHVicy5lUGxhdGZvcm0uU2VydmljZS5EYXRhQ29udHJhY3RzLCBWZXJzaW9uPTIwMTguMC41NDkuMCwgQ3VsdHVyZT1uZXV0cmFsLCBQdWJsaWNLZXlUb2tlbj1udWxsXV0NPVJTQ3B1YnMuZVBsYXRmb3JtLlNlcnZpY2UuRGF0YUNvbnRyYWN0cy5TZWFyY2guQXV0aG9yQ3JpdGVyaWECAAAAPlJTQ3B1YnMuZVBsYXRmb3JtLlNlcnZpY2UuRGF0YUNvbnRyYWN0cy5TZWFyY2guUHVibGljYXRpb25EYXRlAgAAAMIBU3lzdGVtLkNvbGxlY3Rpb25zLkdlbmVyaWMuTGlzdGAxW1tSU0NwdWJzLmVQbGF0Zm9ybS5TZXJ2aWNlLkRhdGFDb250cmFjdHMuRW50aXR5Lk5hbWVWYWx1ZSwgUlNDcHVicy5lUGxhdGZvcm0uU2VydmljZS5EYXRhQ29udHJhY3RzLCBWZXJzaW9uPTIwMTguMC41NDkuMCwgQ3VsdHVyZT1uZXV0cmFsLCBQdWJsaWNLZXlUb2tlbj1udWxsXV0CAAAABgMAAAADQWxsCgYEAAAAA0FsbAkFAAAACQYAAAAAAAAAAAAAAAkHAAAACQgAAAAJCQAAAAoKCgoKBAUAAADCAVN5c3RlbS5Db2xsZWN0aW9ucy5HZW5lcmljLkxpc3RgMVtbUlNDcHVicy5lUGxhdGZvcm0uU2VydmljZS5EYXRhQ29udHJhY3RzLkVudGl0eS5OYW1lVmFsdWUsIFJTQ3B1YnMuZVBsYXRmb3JtLlNlcnZpY2UuRGF0YUNvbnRyYWN0cywgVmVyc2lvbj0yMDE4LjAuNTQ5LjAsIEN1bHR1cmU9bmV1dHJhbCwgUHVibGljS2V5VG9rZW49bnVsbF1dAwAAAAZfaXRlbXMFX3NpemUIX3ZlcnNpb24EAAA6UlNDcHVicy5lUGxhdGZvcm0uU2VydmljZS5EYXRhQ29udHJhY3RzLkVudGl0eS5OYW1lVmFsdWVbXQIAAAAICAkKAAAABAAAAAQAAAABBgAAAAUAAAAJCwAAAAAAAAAAAAAABQcAAAA9UlNDcHVicy5lUGxhdGZvcm0uU2VydmljZS5EYXRhQ29udHJhY3RzLlNlYXJjaC5BdXRob3JDcml0ZXJpYQIAAAAgPEJvb2xlYW5PcGVyYXRvcj5rX19CYWNraW5nRmllbGQYPEF1dGhvcnM + a19fQmFja2luZ0ZpZWxkAQPDAVN5c3RlbS5Db2xsZWN0aW9ucy5HZW5lcmljLkxpc3RgMVtbUlNDcHVicy5lUGxhdGZvcm0uU2VydmljZS5EYXRhQ29udHJhY3RzLlNlYXJjaC5BdXRob3JJbmZvLCBSU0NwdWJzLmVQbGF0Zm9ybS5TZXJ2aWNlLkRhdGFDb250cmFjdHMsIFZlcnNpb249MjAxOC4wLjU0OS4wLCBDdWx0dXJlPW5ldXRyYWwsIFB1YmxpY0tleVRva2VuPW51bGxdXQIAAAAKCgUIAAAAPlJTQ3B1YnMuZVBsYXRmb3JtLlNlcnZpY2UuRGF0YUNvbnRyYWN0cy5TZWFyY2guUHVibGljYXRpb25EYXRlBQAAAB88SXNTZWxlY3RlZERhdGU + a19fQmFja2luZ0ZpZWxkGTxEYXRlVHlwZT5rX19CYWNraW5nRmllbGQbPFdpdGhJbkxhc3Q + a19fQmFja2luZ0ZpZWxkGjxEYXRlUmFuZ2U + a19fQmFja2luZ0ZpZWxkHDxEaXNwbGF5RGF0ZT5rX19CYWNraW5nRmllbGQAAQQEAQE5UlNDcHVicy5lUGxhdGZvcm0uU2VydmljZS5EYXRhQ29udHJhY3RzLlNlYXJjaC5XaXRoSW5MYXN0AgAAADhSU0NwdWJzLmVQbGF0Zm9ybS5TZXJ2aWNlLkRhdGFDb250cmFjdHMuU2VhcmNoLkRhdGVSYW5nZQIAAAACAAAAAAoKCgoBCQAAAAUAAAAJCwAAAAAAAAAAAAAABwoAAAAAAQAAAAQAAAAEOFJTQ3B1YnMuZVBsYXRmb3JtLlNlcnZpY2UuRGF0YUNvbnRyYWN0cy5FbnRpdHkuTmFtZVZhbHVlAgAAAAkMAAAACQ0AAAAJDgAAAAkPAAAABwsAAAAAAQAAAAAAAAAEOFJTQ3B1YnMuZVBsYXRmb3JtLlNlcnZpY2UuRGF0YUNvbnRyYWN0cy5FbnRpdHkuTmFtZVZhbHVlAgAAAAUMAAAAOFJTQ3B1YnMuZVBsYXRmb3JtLlNlcnZpY2UuRGF0YUNvbnRyYWN0cy5FbnRpdHkuTmFtZVZhbHVlBAAAABU8TmFtZT5rX19CYWNraW5nRmllbGQcPERpc3BsYXlOYW1lPmtfX0JhY2tpbmdGaWVsZBY8VmFsdWU + a19fQmFja2luZ0ZpZWxkIDxCb29sZWFuT3BlcmF0b3I + a19fQmFja2luZ0ZpZWxkAQEBAQIAAAAGEAAAAAhmcmVldGV4dAoGEQAAAG9kZXBvc2l0aW9uLCBwYXR0ZXJuLCBmaWxtIEFORCBDdSwgT1IgY29wcGVyLCBPUiBlbGVjdHJvbGVzcywgT1IgcHJpbnRpbmcsIE9SIGZsZXhpYmxlLCBPUiBzdWJzdHJhdGUsIE9SIHBsYXN0aWMKAQ0AAAAMAAAABhIAAAAHQWxsVGV4dAoGEwAAABlkZXBvc2l0aW9uLCBwYXR0ZXJuLCBmaWxtCgEOAAAADAAAAAYUAAAAC0F0bGVhc3RUZXh0CgYVAAAAP0N1LCBjb3BwZXIsIGVsZWN0cm9sZXNzLCBwcmludGluZywgZmxleGlibGUsIHN1YnN0cmF0ZSwgcGxhc3RpYwoBDwAAAAwAAAAGFgAAABBPcmlnaW5hbEZyZWVUZXh0CgYXAAAAb2RlcG9zaXRpb24sIHBhdHRlcm4sIGZpbG0gQU5EIEN1LCBPUiBjb3BwZXIsIE9SIGVsZWN0cm9sZXNzLCBPUiBwcmludGluZywgT1IgZmxleGlibGUsIE9SIHN1YnN0cmF0ZSwgT1IgcGxhc3RpYwoL',
        'resultcount': '282607',
        'category': 'all',
        'pageno': '2'
    }

    html = requests.post(url, data=data, headers=headers1, stream=True, timeout=20, verify=True)
    html.encoding = 'utf-8'
    text = html.text
    # print(text)
    bsop = BeautifulSoup(text, 'html.parser')
    divs = bsop.findAll('div', {'class': 'capsule capsule--article '})
    for i in divs:
        article_url = 'https://pubs.rsc.org' + i.find('a').attrs['href']
        print(article_url)
        # royal(article_url)

    # with open("ros.html", 'wb') as f:
    #     f.write(html.content)
    #     f.close()
    # print(text)

# session.head('https://pubs.rsc.org/en/results/all?Category=All&AllText=deposition%2C%20pattern%2C%20film&AtleastText=Cu%2C%20copper%2C%20electroless%2C%20printing%2C%20flexible%2C%20substrate%2C%20plastic&IncludeReference=false&SelectJournal=false&DateRange=false&SelectDate=false&Type=Months&DateFromMonth=Months&DateToMonth=Months&PriceCode=False&OpenAccess=false')

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

url = 'https://pubs.rsc.org/en/search/journalresult'
scawurls(url)



# url = 'https://pubs.rsc.org/en/content/articlelanding/2017/tc/c7tc00038c#!divAbstract'
# royal(url)

# nums = 5
# # 图片存储路径，在linux系统下
# file_path = '/home/zhangyb/downloadfiles/pythonpro/biaoqing'
# # 图片存储路径，在windows系统下
# # file_path = 'E:\downloadfiles\pythonpro\biaoqing'
# urls = scrapy_img_urls(nums)
# for i in urls:
#     print(i)
#     download_img_url(i)


# url = 'https://pubs.rsc.org/en/results/all?Category=All&AllText=deposition%2C%20pattern%2C%20film&AtleastText=Cu%2C%20copper%2C%20electroless%2C%20printing%2C%20flexible%2C%20substrate%2C%20plastic&IncludeReference=false&SelectJournal=false&DateRange=false&SelectDate=false&Type=Months&DateFromMonth=Months&DateToMonth=Months&PriceCode=False&OpenAccess=false'
# r = requests.get(url, headers=headers)
# print(r.text)
