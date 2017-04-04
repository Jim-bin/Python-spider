# -*- coding: utf-8 -*-

'''
python 2.7.12
'''

import requests
from parsel import Selector
import time
import re, random, os


def scraw_pin_ids():

	pin_ids = []
	pin_id = '1068018182'

	flag = True
	while flag:
		try:
			url = "http://huaban.com/favorite/beauty/"
			headers1 = {
			'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
			'Accept':'application/json',
			'X-Request':'JSON',
			'X-Requested-With':'XMLHttpRequest',
			}

			params = {
				'j0l4lymf':'',
				'max':pin_id,
				'limit':'20',
				'wfl':'1',
			}

			z1 = requests.get(url, params=params, headers=headers1)

			if z1.json()['pins']:
				for i in z1.json()['pins']:
					pin_ids.append(i['pin_id'])
					pin_id = pin_ids[-1]
					print i['pin_id']
					# with open("pin_ids.txt",'ab') as f:
					# 	f.write(str(i['pin_id'])+"\n")
					# 	f.close()
					time.sleep(0.001)
			else:
				flag = False
				return set(pin_ids)
		except:
			continue

def scraw_urls(pin_ids):

	urls = []

	urlss = ['http://huaban.com/pins/' + str(i) +'/' for i in pin_ids]
	for url in urlss:
		try:
			headers = {
			'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
			}

			z3 = requests.get(url, headers=headers)

			text = z3.text

			pattern = re.compile('"key":"(.*?)"', re.S)
			items = re.findall(pattern, text)

			urls.extend(items)
			print items
			print '============================================================================================================'
		except:
			continue
	return set(urls)

def download(urls):
	headers1 = {
	'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
	}
	n = 1
	urls = set(urls)
	for url in urls:
		try:
			if not os.path.exists(os.path.join(file_path, "huaban")):
				os.makedirs(os.path.join(file_path, "huaban"))
			os.chdir(file_path + '\\' + "huaban")
			try:
				url = 'http://img.hb.aicdn.com/' + url
				r = requests.get(url, headers=headers1)
				if len(r.content)>40000:
					with open(str(n)+".jpg", 'wb') as f:
						f.write(r.content)
						f.close()
						print u"第" + str(n) + u"张图片下载成功"
						n+=1
						# time.sleep(3)
			except:
				continue
		except:
			continue

# 图片存储路径
file_path = 'E:\selfprogress\programming\project\pa1024\huabannnnnnn'
pin_ids = scraw_pin_ids()
urls = scraw_urls(pin_ids)
download(urls)
