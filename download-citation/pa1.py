# -*- coding: utf-8 -*-

import requests
import random
from bs4 import BeautifulSoup
import time

download_time = time.strftime("%Y-%m-%d", time.localtime())


def royal(article_urls):
    for article_url in article_urls:
        # try:
        html = requests.get(article_url, headers=headers, stream=True, timeout=20, verify=True)
        html.encoding = 'utf-8'
        text = html.text
        bsop = BeautifulSoup(text, 'html.parser')
        try:
            timeofissued = bsop.find('meta', {'name':'DC.issued'}).attrs['content'].split('/')[0]
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
            citation_issue = bsop.find('meta', {'name':'citation_issue'}).attrs['content']
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
            PB = bsop.find('meta', {'name':'DC.publisher'}).attrs['content']
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
            citation_abstract = bsop.find('meta', {'name':'citation_abstract'}).attrs['content'].strip()
        except:
            pass
        try:
            SN = bsop.find('div', {'class':'article-nav__issue autopad--h'}).find('a').attrs['href'].split('=')[-1]
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

            authors = bsop.findAll('span', {'class': 'article__author-link'})
            for author in authors:
                author = author.find('a').text.split(' ')
                author = author[-1] + ', ' + ' '.join(author[:-1])
                f.write('A1  - ' + author + '\n')
            f.write('ER  - ' + '\n\n\n')
            f.close()
        time.sleep(1)


def crawl_article_url(nums):
    article_urls = []
    for num in range(1, nums+1):

        url = 'https://pubs.rsc.org/en/search/journalresult'

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
            'pageno': str(num)
        }

        html = requests.post(url, data=data, headers=headers1, stream=True, timeout=20, verify=True)
        html.encoding = 'utf-8'
        text = html.text
        # print(text)
        bsop = BeautifulSoup(text, 'html.parser')
        divs = bsop.findAll('div', {'class': 'capsule capsule--article '})
        for i in divs:
            article_url = 'https://pubs.rsc.org' + i.find('a').attrs['href']
            # print(article_url)
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
nums = 5  # 爬取的页数

article_urls = crawl_article_url(nums)
royal(article_urls)



# url = 'https://pubs.rsc.org/en/content/articlelanding/2017/tc/c7tc00038c#!divAbstract'
# royal(url)
