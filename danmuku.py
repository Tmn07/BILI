# -*- coding: utf-8 -*-
"""
Created on Sat Apr 09 02:27:43 2016
@author: Tmn07
@update: 2019/02/08 20点57分
"""

from bs4 import BeautifulSoup
import requests
import argparse

import re
import time

def write_down(html, filename='test.html'):
    with open(filename, 'w') as f:
        f.write(html)

header = {
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Referer': 'http://www.bilibili.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:45.0) Gecko/20100101 Firefox/45.0'
}

def get_danmuku(cid, filename):
    danmuku_api = "https://api.bilibili.com/x/v1/dm/list.so?oid="
    r2 =requests.get(danmuku_api+cid, headers=header)
    soup = BeautifulSoup(r2.content, 'lxml')
    danmus = soup.find_all('d')
    with open(filename, 'w') as fw:
        print(u"写入弹幕ing...")
        for danmu in danmus:
            content = danmu.string
            attr = danmu['p'].split(',')
            t1 = str(attr[0])  # 视频中的时间
            t2 = attr[4]  # 发布时间
            timestr = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(t2)))
            fw.write(content.encode('utf-8')+ ',' + t1 + ',' + timestr + '\n')
    print(u"写入完成...请查看"+filename)   

# mode 1 是输入av12345678
# mode 2 是输入ep1234567 （番剧）
def get_cid(aid, mode=1):
    # print(aid)
    if mode == 1:
        url = "https://www.bilibili.com/video/av"+aid
        r = requests.get(url, headers=header)
        match_list = re.findall('"aid":"'+aid+'".*?"cid":\d*?,', r.text)
    elif mode == 2:
        url = "https://www.bilibili.com/bangumi/play/ep"
        r = requests.get(url+aid, headers=header)
        match_list = re.findall(',"id":'+aid+'.*?"cid":\d*?,', r.text)
        # write_down(r.content)
    # print (match_list)
    cid = match_list[0][match_list[0].index('cid')+5:-1]
    print ("cid = " + cid)
    return cid

def get_input_id():
    parser = argparse.ArgumentParser(description='Welcome to BILI')
    parser.add_argument('-i', '--input', help='set the av_number or eq_number to crawl')
    parser.add_argument('-o', '--output',  help='set the filename to store')
    args = parser.parse_args()
    if args.output:
        filename = args.output
    else:
        filename = 'test.csv'
    aid = str(args.input)
    if aid.startswith('av'):
        return (aid[2:], 1, filename)
    if aid.startswith('ep'):
        return (aid[2:], 2, filename)
    return (aid, 1, filename)

def main():
    aid, mode, filename = get_input_id()
    cid = get_cid(aid, mode)
    get_danmuku(cid, filename)
    
if __name__ == '__main__':
    main()