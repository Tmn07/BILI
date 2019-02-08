#coding=utf-8

import requests
import json

def read_cookie(cookiepath):
	with open(cookiepath, 'r') as fid:
		cookies = fid.readlines()
	return cookies

def do_sign(headers):
	url_live = "https://api.live.bilibili.com/sign/doSign"
	r = requests.get(url_live, headers=headers)
	print('doSign: ' + json.loads(r.text)['msg'])

def silver2coin(headers):
	url_coin = "https://api.live.bilibili.com/pay/v1/Exchange/silver2coin"
	r = requests.get(url_coin, headers=headers)
	print('silver2coin: ' + json.loads(r.text)['msg'])

if __name__=='__main__':
	cookies = read_cookie('./bilicookies')[0]
	headers = {
	    'accept-encoding': 'gzip, deflate, sdch',
	    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.16 Safari/537.36',
	    'authority': 'live.bilibili.com',
	    'cookie': cookies,
	}
	do_sign(headers)
	# silver2coin(headers)
