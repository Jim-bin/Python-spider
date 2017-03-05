# -*- coding: utf-8 -*-

'''
python 3.5.2
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

def download_img(img_list, img_title):
    '''
    通过scrawl_url函数获得了单个图册里面所有图片的url列表和图册的名字，就可以下载图片了
    此函数的作用下载单个图册里面的所有图片
    接收参数img_list是单个图册里面所有图片的的url，
    如['http://mm.howkuai.com/wp-content/uploads/2017a/02/07/01.jpg',
    'http://mm.howkuai.com/wp-content/uploads/2017a/02/07/02.jpg',...]
    img_title是单个图册的名字，如’香车美女，最完美的黄金搭档‘
    :param img_list:
    :param img_title:
    :return:
    '''

    img_title = format_name(img_title) # 如果图册名字有特殊字符需要处理。不然在windows下保存不了文件夹
    for img_urls in img_list:
        img_url = img_urls.attrs['src'] # 单个图片的url地址
        print(img_url)
        title = img_urls.attrs['alt'] # 单个图片的名字
        print(title)

        try:
            if not os.path.exists(os.path.join(file_path, img_title)):
                os.makedirs(os.path.join(file_path, img_title))
            os.chdir(file_path + '\\' + img_title)

            # 图片保存到本地
            exists = os.path.exists(img_title)
            if not exists:
                try:
                    img_html = requests.get(img_url, headers=headers, stream=True, timeout=20, verify=True)
                    with open(title+".jpg", 'wb') as f:
                        f.write(img_html.content)
                        f.close()
                except:
                    continue
        except:
            continue

def scrawl_list(url_list, proxy_flag=False, try_time=0):
    '''
    此函数的作用是爬取每一页面所有图册的url，一个页面包含10个图册，所有调用一次函数则返回一个包含10个url的列表
    格式如['http://www.meizitu.com/a/list_1_1.html',...]
    :param url_list:
    :param proxy_flag:
    :param try_time:
    :return:
    '''
    if not proxy_flag:  # 不使用代理
        try:
            html = requests.get(url_list, headers=headers,  timeout=10)
            html.encoding = 'gb2312'
            text = html.text

            bsop = BeautifulSoup(text, 'html.parser')

            url_imgs = []
            li_list = bsop.find('ul', {'class': 'wp-list clearfix'}).findAll('li', {'class':'wp-item'})
            for i in li_list:
                url_img = i.find('h3',{'class':'tit'}).find('a').attrs['href']
                url_imgs.append(url_img)
            return url_imgs
        except:
            return scrawl_list(url_list, proxy_flag=True)  # 否则调用自己，使用3次IP代理
    else:   # 使用代理时
        if try_time<count_time:
            try:
                print('尝试第'+str(try_time+1)+'次使用代理下载')
                html = requests.get(url_list, headers=headers, proxies={'http': get_random_ip()}, timeout=10)
                html.encoding = 'gb2312'
                text = html.text

                bsop = BeautifulSoup(text, 'html.parser')

                url_imgs = []
                # url_titles = []
                li_list = bsop.find('ul', {'class': 'wp-list clearfix'}).findAll('li', {'class': 'wp-item'})
                for i in li_list:
                    url_img = i.find('h3', {'class': 'tit'}).find('a').attrs['href']
                    url_imgs.append(url_img)
                print('状态码为'+str(html.status_code))
                if html.status_code==200:
                    print('url_imgs通过IP代理处理成功！')
                    return url_imgs  # 代理成功下载！
                else:
                    return scrawl_list(url_list, proxy_flag=True, try_time=(try_time + 1))
            except:
                print('url_imgs代理下载失败，尝试下次代理')
                return scrawl_list(url_list, proxy_flag=True, try_time=(try_time+1))  # 否则调用自己，使用3次IP代理
        else:
            print('url_imgs爬取失败，请检查网页')
            return None

def scrawl_url(url, proxy_flag=False, try_time=0):
    '''
    此函数的作用是爬取单个图册里面的所有图片的url，一个图册包含几张图片，每个图片有个真实的url地址，需要获取得到
    此函数接收图册url作为参数，如'http://www.meizitu.com/a/5499.html',返回该图册里面所有图片的url列表和图册的名字
    所有图片共用一个名字，可作为文件夹名字存储
    :param url:
    :param proxy_flag:
    :param try_time:
    :return:
    '''
    if not proxy_flag:  # 不使用代理
        try:
            html = requests.get(url, headers=headers,  timeout=10)
            html.encoding = 'gb2312'
            text = html.text

            bsop = BeautifulSoup(text, 'html.parser')
            img_list = bsop.find('div', {'class': 'postContent'}).find('p').findAll('img')
            img_title = bsop.find('div', {'class': 'metaRight'}).find('h2').find('a').text

            return img_list, img_title

        except:
            return scrawl_url(url, proxy_flag=True)  # 否则调用自己，使用3次IP代理
    else:   # 使用代理时
        if try_time<count_time:
            try:
                print('尝试第'+str(try_time+1)+'次使用代理下载')

                html = requests.get(url, headers=headers, proxies={'http': get_random_ip()},timeout=30)
                html.encoding = 'gb2312'

                text = html.text
                bsop = BeautifulSoup(text, 'html.parser')
                img_list = bsop.find('div', {'class': 'postContent'}).find('p').findAll('img')
                img_title = bsop.find('div', {'class': 'metaRight'}).find('h2').find('a').text

                print('状态码为'+str(html.status_code))
                if html.status_code==200:
                    print('图片通过IP代理处理成功！')
                    return img_list, img_title  # 代理成功下载！
                else:
                    return scrawl_url(url, proxy_flag=True, try_time=(try_time + 1))
            except:
                print('IP代理下载失败')
                return scrawl_url(url, proxy_flag=True, try_time=(try_time+1))  # 否则调用自己，使用3次IP代理
        else:
            print('图片url列表未能爬取，请检查网页')
            return None

def download_urls(pages):
    '''
     此函数的作用是爬取所有页面的url，最后返回的是包含所有页面url的二位列表，格式如下
     url_imgss = [
                  ['http://www.meizitu.com/a/list_1_1.html',...],
                  ['http://www.meizitu.com/a/list_1_2.html',...],
                  ...
                 ]
    '''
    url_imgss = []
    for i in range(1, pages+1):
        try:
            url_list = 'http://www.meizitu.com/a/list_1_' + str(i) + '.html'
            url_imgs = scrawl_list(url_list)
            if not url_imgs:
                continue
            url_imgss.append(url_imgs)
            print("第"+str(i)+"页url爬取成功")
            time.sleep(5)   #休息5秒篇爬取下一页
        except: # 如果其中某一页出错，则跳过该页，继续爬取下一页，从而不使程序中断
            continue
    return url_imgss

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

def get_total_pages(first_url):
    '''
    获取妹子图所有页面
    :param first_url:
    :return:
    '''
    html = requests.get(first_url, headers=headers, timeout=10)
    html.encoding = 'gb2312'
    text = html.text
    bsop = BeautifulSoup(text, 'html.parser')
    lis =bsop.find('div',{'id':'wp_page_numbers'}).find('ul').findAll('li')
    pages = lis[-1].find('a').attrs['href'].split('.')[0].split('_')[-1]
    pages = int(pages)
    return pages


# 妹子图的首页，用来获取总的页数
first_url = 'http://www.meizitu.com/a/list_1_1.html'

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

# 图片存储路径
file_path = 'E:\selfprogress\programming\project\meizitu'

# 获取总页数
pages = get_total_pages(first_url)

# 爬取IP代理
total_ip = scrawl_ip(url_ip, num)

# 带爬取的url
url_imgss = download_urls(pages)

for i in url_imgss:
    for j in i:
        try:
            with open('url.txt','a') as f:
                f.write(j+"\n")
                f.close()
                print("写入url.txt文件成功")
        except:
            print("写入url.txt文件失败")

for url_imgs in url_imgss:
    for url_img in url_imgs:
        img_list, img_title = scrawl_url(url_img)
        if not img_list:
            continue
        download_img(img_list, img_title)

        time.sleep(5)





