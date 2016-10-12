# -*- coding: utf-8 -*-
"""
Created on 2016-08-17

@author: Tmn07
"""

import sys
# reload(sys)
# sys.setdefaultencoding("utf-8")

import time
import requests
from bs4 import BeautifulSoup

def read_cookie(cookiepath):
	with open(cookiepath, 'r') as fid:
		cookies = fid.readlines()
	return cookies

class BILI(object):
	def __init__(self,Cookie):
		self.s = requests.Session()
		self.Cookie = Cookie

	def login(self):
		pass

	def get_comment_num(self,av_num):

		try:
			r = self.s.get('http://api.bilibili.com/x/v2/reply?jsonp=jsonp&type=1&sort=0&oid='+av_num)
			replies = r.json()['data']['replies']
			if replies == []:
				return 0
			else:
				return replies[0]['floor']

			# return r.json()['data']['page']['count']

		except Exception as e:
			print(e)
			return None
			# exit()
		
	def send_comment(self,av_num,message):
		
		header ={
			'Accept':'application/json, text/javascript, */*; q=0.01',
			'Accept-Encoding':'gzip, deflate',
			'Accept-Language':'zh-CN,zh;q=0.8',
			'Cache-Control':'max-age=0',
			'Content-Length': '91',
			'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
			'Connection':'keep-alive',
			'Cookie':self.Cookie,
			'Host':'api.bilibili.com',
			'Origin': 'http://www.bilibili.com',
			'Referer':'http://www.bilibili.com/video/av'+av_num+'/',
			'Upgrade-Insecure-Requests':'1',
			'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36 '
		}

		post_data = {
			'jsonp':'jsonp',
			'message':message,
			'type':'1',
			'plat':'1',
			'oid':av_num
		}

		comment_url = "http://api.bilibili.com/x/reply/add"

		try:
			r = self.s.post(comment_url,headers=header,data=post_data)
			if r.json()['message'] == 'ok':
				print('ok')
			else:
				print('error-5')
		except Exception as e:
			print(e)
			# exit()

	def get_newest(self):
		header = {
			'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
			'Accept-Encoding':'gzip, deflate, sdch',
			'Accept-Language':'zh-CN,zh;q=0.8',
			'Cache-Control':'max-age=0',
			'Connection':'keep-alive',
			'Cookie':self.Cookie,
			'Upgrade-Insecure-Requests':'1',
			'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36'
		}
		# 注意type=1时不含番剧信息
		url = "http://api.bilibili.com/x/feed/pull?jsonp=jsonp&ps=10&type=0"
		try:
			r = self.s.get(url,headers=header)
			av_num = r.json()['data']['feeds'][0]['add_id']
			return str(av_num)
		except Exception as e:
			print(e)
			# exit()

	def get_dynamic(self):
		# todo: get newest av number——也许有api。。
		# 获取得这个'动态'页面
		# 查看最新更新得视频。

		header ={
			'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
			'Accept-Encoding':'gzip, deflate, sdch',
			'Accept-Language':'zh-CN,zh;q=0.8',
			'Cache-Control':'max-age=0',
			'Connection':'keep-alive',
			'Cookie':self.Cookie,
			'Host':'www.bilibili.com',
			'Referer':'http://www.bilibili.com/',
			'Upgrade-Insecure-Requests':'1',
			'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36 '
			}

		url = "http://www.bilibili.com/account/dynamic"
		try:
			r = self.s.get(url,headers=header)
			content = r.text
			soup = BeautifulSoup(content,'lxml')
		except Exception as e:
			raise e
			exit()

	# 快速模式，慢速模式。。
	def run(self,av_num=None,floor=0):
		if av_num is None:
			while 1:
				av_num = self.get_newest()
				print(av_num)
				comment_num = self.get_comment_num(av_num)
				print(comment_num)
				if comment_num==0:
					self.send_comment(av_num,'1楼精准打击～没有人能在我的关注里打败我，大大的flag233')

					with open('result.txt','a') as f:
						f.write(av_num)
						f.close()
					# break
				time.sleep(1)
		else:		

			if floor != 0:
				while 1:
					comment_num = self.get_comment_num(av_num)
					print(comment_num)
					if comment_num+1 == floor:
						self.send_comment(av_num,str(floor)+'楼精准打击～')
						break
					if comment_num >= floor:
						print('被别人抢了。。')
						break
					time.sleep(5)


if __name__=='__main__':
	cookies = read_cookie('./bilicookies')[0]
	bi = BILI(cookies)
	
	# bi.run()
	# bi.run('5817722',floor=1000)
	bi.run(floor=1)