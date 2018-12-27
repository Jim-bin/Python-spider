# -*- coding:utf-8 -*_

import requests, time
import hmac, json
from bs4 import BeautifulSoup
from hashlib import sha1

def get_captcha(url):
    ''' 处理验证码 '''

    r = requests.get(url, headers=headers)
    text = r.text
    obj = BeautifulSoup(text, 'html.parser')
    captchaurl = 'http://zhjwxk.cic.tsinghua.edu.cn' + obj.find("img", {"id":"captcha"}).attrs['src']
    rr = requests.get(captchaurl, headers=headers)
    textt = rr.content

    with open('captcha.gif', 'wb') as fb:
        fb.write(textt)
        a = input('captcha:')
        print(a)
    return a


s = requests.Session()
url = 'https://zhjwxk.cic.tsinghua.edu.cn/j_acegi_formlogin_xsxk.do'

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Content-Length': '66',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Cookie': 'JSESSIONID=cafgDstvY9fVWd2VutTFw; thuwebcookie=990146470.20480.0000',
    'DNT': '1',
    'Host': 'zhjwxk.cic.tsinghua.edu.cn',
    'Origin': 'http://zhjwxk.cic.tsinghua.edu.cn',
    'Referer': 'http://zhjwxk.cic.tsinghua.edu.cn/xklogin.do',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
}
data = {
    'j_username': 'zhang-yb18',
    'j_password': 'ZHANG2338',
    'captchaflag': 'login1',
    '_login_image_': get_captcha(url),
}


r = s.post(url, headers=headers, data=data)
text = r.text
print(text)