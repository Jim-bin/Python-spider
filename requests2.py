# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup


url = 'http://tieba.baidu.com/p/4468445702'
html = requests.get(url)
html.encoding = 'utf-8'

text = html.text
bsop = BeautifulSoup(text,'html.parser')
img_list = bsop.find('div',{'id':'post_content_87286618651'}).findAll('img')
img_src = img_list[0].attrs['src']

print(img_src)
img = requests.get(img_src)
with open('a.jpg', 'ab') as f:
    f.write(img.content)
    f.close()


# content = html.content
# print(text)
# print(content)