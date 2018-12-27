# -*- coding:utf-8 -*_

from selenium import webdriver

import requests

from time import sleep

from bs4 import BeautifulSoup

browser = webdriver.Chrome(executable_path='F:\\pro\\blog\herokublog\\blogtestgithub\\royal\\chromedriver.exe')

url= 'https://www.zhihu.com/'

s = requests.Session()

s.headers.clear()#清除requests头部中的Python机器人信息，否则登录失败

browser.get(url)

browser.find_element_by_xpath('//*[@id="root"]/div/main/div/div/div/div[2]/div[2]/span').click()#避免屏幕失去焦点

browser.find_element_by_xpath('//*[@id="root"]/div/main/div/div/div/div[2]/div[1]/form/div[1]/div[2]/div[1]/input').send_keys('fendushu@163.com')

browser.find_element_by_xpath('//*[@id="root"]/div/main/div/div/div/div[2]/div[1]/form/div[2]/div/div[1]/input').send_keys('ZHANG2338')

try:

  img = browser.find_element_by_xpath('//*    [@id="root"]/div/main/div/div/div/div[2]/div[1]/form/div[3]/div/div[2]/img')#验证码图片链接--倒立文字

  sleep(10)

except:

  img= browser.find_element_by_xpath('//*[@id="root"]/div/main/div/div/div/div[2]/div[1]/form/div[3]/div/span/div/img').get_attribute("src")#验证码图片链接--字母数字

  sleep(10)#填写验证码

else:

  pass

browser.find_element_by_xpath('//*[@id="root"]/div/main/div/div/div/div[2]/div[1]/form/button').submit()#登录

sleep(5)#等待Cookies加载

cookies = browser.get_cookies()

browser.quit()

for cookie in cookies:
    s.cookies.set(cookie['name'],cookie['value'])#为session设置cookies

html=s.get(url).text

soup = BeautifulSoup(html)

items = soup.find_all('a',attrs={'data-za-detail-view-element_name':"Title"})#获取登录后加载出的前几个话题的标题

for item in items:
    print(item.string)

