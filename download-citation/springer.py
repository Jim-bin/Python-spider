# -*- coding: utf-8 -*-

import requests
import random
from bs4 import BeautifulSoup
import time

download_time = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())


def royal(article_urls):
    for article_url in article_urls:
        # try:
        html = requests.get(article_url, headers=headers, stream=True, timeout=20, verify=True)
        html.encoding = 'utf-8'
        text = html.text
        bsop = BeautifulSoup(text, 'html.parser')
        try:
            timeofissued = bsop.find('meta', {'name':'citation_cover_date'}).attrs['content'].split('/')[0]
        except:
            pass
        try:
            citation_title = bsop.find('meta', {'name':'citation_title'}).attrs['content']
        except:
            pass
        try:
            citation_journal_title = bsop.find('meta', {'name':'citation_journal_title'}).attrs['content']
        except:
            pass
        try:
            citation_journal_abbrev = bsop.find('meta', {'name':'citation_journal_abbrev'}).attrs['content']
        except:
            pass
        try:
            citation_volume = bsop.find('meta', {'name':'citation_volume'}).attrs['content']
        except:
            pass
        try:
            # citation_issue = bsop.find('meta', {'name':'citation_issue'}).attrs['content']
            citation_issue = bsop.find('span', {'id':'electronic-issn'}).text
        except:
            pass
        try:
            citation_firstpage = bsop.find('meta', {'name':'citation_firstpage'}).attrs['content']
        except:
            pass
        try:
            citation_lastpage = bsop.find('meta', {'name':'citation_lastpage'}).attrs['content']
        except:
            pass
        try:
            citation_doi = bsop.find('meta', {'name':'citation_doi'}).attrs['content']
        except:
            pass
        try:
            PB = bsop.find('meta', {'name':'citation_publisher'}).attrs['content']
        except:
            pass
        try:
            M3 = citation_doi
        except:
            pass
        try:
            citation_url = 'http://dx.doi.org/' + citation_doi
        except:
            pass
        try:
            # citation_abstract = bsop.find('p', {'id':'Par1'}).attrs['content'].strip()
            citation_abstract = bsop.find('p', {'id':'Par1'}).text
        except:
            pass
        try:
            # SN = bsop.find('div', {'class':'article-nav__issue autopad--h'}).find('a').attrs['href'].split('=')[-1]
            SN = bsop.find('span', {'id':'electronic-issn'}).text
        except:
            pass
        # except:
        #     print(article_url)
        #     continue

        with open(download_time + ".ris", 'a', encoding='utf-8') as f:
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
            # print(citation_abstract)

            authors = bsop.findAll('meta', {'name': 'citation_author'})
            for author in authors:
                # print(author)
                author = author.attrs['content']
                # print(author)
                author = author[-1] + ', ' + ' '.join(author[:-1])
                f.write('A1  - ' + author + '\n')
            f.write('ER  - ' + '\n\n\n')
            f.close()
        time.sleep(1)


def crawl_article_url(nums):
    article_urls = []
    for num in range(1, nums+1):

        url = 'https://link.springer.com/search/page/' + str(num) + '?date-facet-mode=between&facet-start-year=2010&facet-language=%22En%22&query=printing%2C+AND+Cu+AND+pattern%2C+AND+film%2C+AND+flexible%2C+AND+plastic%2C+AND+substrate%2C+AND+copper&facet-end-year=2019&showAll=true&facet-content-type=%22Article%22'

        html = requests.get(url, headers=headers, stream=True, timeout=20, verify=True)
        html.encoding = 'utf-8'
        text = html.text
        # print(text)
        bsop = BeautifulSoup(text, 'html.parser')
        divs = bsop.find('ol', {'id': 'results-list'}).findAll('li')
        for i in divs:
            # print(i)
            article_url = 'https://link.springer.com' + i.find('h2').find('a').attrs['href']
            print(article_url)
            article_urls.append(article_url)
        print("第" + str(num) + "页爬取完毕")
        time.sleep(1)
    return article_urls


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
nums = 1  # 爬取的页数

article_urls = crawl_article_url(nums)
royal(article_urls)