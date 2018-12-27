# -*- coding:UTF-8 -*-

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
    return input('captcha:')





def login(username, password, oncaptcha, sessiona, headers):
    ''' 处理登录 '''

    resp1 = sessiona.get('https://www.zhihu.com/signin', headers=headers)  # 拿cookie:_xsrf
    resp2 = sessiona.get('https://www.zhihu.com/api/v3/oauth/captcha?lang=cn',
                         headers=headers)  # 拿cookie:capsion_ticket
    need_cap = json.loads(resp2.text)["show_captcha"]  # {"show_captcha":false} 表示不用验证码

    grantType = 'password'
    clientId = 'c3cef7c66a1843f8b3a9e6a1e3160e20'
    source = 'com.zhihu.web'
    timestamp = str((time.time() * 1000)).split('.')[0]  # 签名只按这个时间戳变化

    captcha_content = sessiona.get('https://www.zhihu.com/captcha.gif?r=%d&type=login' % (time.time() * 1000),
                                   headers=headers).content

    data = {
        "client_id": clientId,
        "grant_type": grantType,
        "timestamp": timestamp,
        "source": source,
        "signature": get_signature(grantType, clientId, source, timestamp),  # 获取签名
        "username": username,
        "password": password,
        "lang": "cn",
        "captcha": oncaptcha(captcha_content, need_cap),  # 获取图片验证码
        "ref_source": "other_",
        "utm_source": ""
    }

    print("**2**: " + str(data))
    print("-" * 50)
    resp = sessiona.post('https://www.zhihu.com/api/v3/oauth/sign_in', data, headers=headers).content
    print(BeautifulSoup(resp, 'html.parser'))

    print("-" * 50)
    return resp



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
    '_login_image_': get_captcha,
}


if __name__ == "__main__":
    sessiona = requests.Session()

    login('fendushu@163.com', 'ZHANG2338', get_captcha, sessiona, headers)  # 用户名密码换自己的就好了
    resp = sessiona.get('https://www.zhihu.com/inbox', headers=headers)  # 登录进去了，可以看私信了
    print(BeautifulSoup(resp.content, 'html.parser'))

