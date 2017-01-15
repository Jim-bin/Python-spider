# -*- coding: utf-8 -*-

# 导入模块
import time
import requests, re, random, os
from bs4 import BeautifulSoup

def ip_test(ip, url_for_test='https://www.baidu.com', set_timeout=30):
    try:
        r = requests.get(url_for_test, headers=headers, proxies={'http': ip[0]+':'+ip[1]}, timeout=set_timeout)
        if r.status_code == 200:
            return True
        else:
            return False
    except:
        return False

def scrawl_ip(url, num, url_for_test='https://www.baidu.com'):
    ip_list = []
    for num_page in range(1, num):
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

    time.sleep(10)  # 等待10秒爬取下一页

def get_random_ip():    # 随机获取一个IP
    ind = random.randint(0, len(total_ip)-1)
    # print(total_ip[ind])
    return total_ip[ind]


def download_img(img_list):
    img_title = img_list[0].attrs['alt']
    for img_url in img_list:
        img_url = img_url.attrs['src']
        title = img_url.split('/')[-1]

        if not os.path.exists(os.path.join(file_path, img_title)):
            os.makedirs(os.path.join(file_path, img_title))
        os.chdir(file_path + '\\' + img_title)

        # 图片保存到本地
        exists = os.path.exists( title)
        if not exists:
            img_html = requests.get(img_url, headers=headers, stream=True, timeout=30, verify=True)
            with open(title, 'wb') as f:
                f.write(img_html.content)
                f.close()

def scrawl_url(url, proxy_flag=False, try_time=0):
    if not proxy_flag:  # 不使用代理
        try:
            html = requests.get(url, headers=headers,  timeout=30)
            html.encoding = 'gb2312'

            text = html.text
            code = html.status_code
            print(code)
            bsop = BeautifulSoup(text, 'html.parser')
            img_list = bsop.find('div', {'class': 'postContent'}).find('p').findAll('img')

            return img_list

        except:
            return scrawl_url(url, proxy_flag=True)  # 否则调用自己，使用3次IP代理
    else:   # 使用代理时
        if try_time<count_time:
            try:
                print('尝试第'+str(try_time+1)+'次使用代理下载')
                # IP_address=get_random_IP()[0]
                html = requests.get(url, headers=headers, proxies={'http': get_random_ip()},timeout=30)
                html.encoding = 'gb2312'

                text = html.text
                code = html.status_code
                print(code)
                bsop = BeautifulSoup(text, 'html.parser')
                img_list = bsop.find('div', {'class': 'postContent'}).find('p').findAll('img')

                print('状态码为'+str(html.status_code))
                if html.status_code==200:
                    print('图片通过IP代理处理成功！')
                    return img_list  # 代理成功下载！
                else:
                    return scrawl_url(url, proxy_flag=True, try_time=(try_time + 1))
            except:
                print('IP代理下载失败')
                return scrawl_url(url, proxy_flag=True, try_time=(try_time+1))  # 否则调用自己，使用3次IP代理
        else:
            print('图片未能下载')
            return None

def scrawl_title(img_list):
    img_title = img_list[0].attrs['alt']
    return img_title

# 爬取代理的url
url_ip = "http://www.xicidaili.com/nt/"

# 设定等待时间
set_timeout = 30

# 爬取代理的页数，2表示爬取2页的ip地址
num = 3

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
headers = {'User-Agent':random.choice(UserAgent_List),
            'Accept':"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            'Accept-Encoding':'gzip',
          }

file_path='E:\selfprogress\programming\project\pa1024\meizitu'  # 存储的地址

# 带爬取的url
for i in range(10,20):
    url = 'http://www.meizitu.com/a/' + str(i) + '.html'

    total_ip = scrawl_ip(url_ip, num)
    img_list = scrawl_url(url)

    download_img(img_list)

    time.sleep(10)





