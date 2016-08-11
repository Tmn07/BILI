# -*- coding: utf-8 -*-
"""
Created on Sat Apr 09 02:27:43 2016

@author: Tmn07
"""
from bs4 import BeautifulSoup
import urllib2
from StringIO import StringIO
import gzip
import zlib
import re

import time

import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

class BILI(object):
    def __init__(self):
        pass

    def gzip_url(self,url):
        header = {
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Accept-Encoding': 'gzip',
            'Referer': 'http://www.bilibili.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:45.0) Gecko/20100101 Firefox/45.0'
        }
        request = urllib2.Request(url,headers=header)
        response = urllib2.urlopen(request)
        # gzip解压
        if response.info().get('Content-Encoding') == 'gzip':
            compresseddata = response.read()
            buf = StringIO(compresseddata)
            f = gzip.GzipFile(fileobj=buf)
            data = f.read()
        # deflate解压
        else:
            data = zlib.decompress(response.read(),-zlib.MAX_WBITS)
        return data

    def set_url(self,url):
        html = self.gzip_url(url)
        print '视频页面 gzip解压完成...'

        soup = BeautifulSoup(html,"lxml")
        try:
            da1 = soup.find('div',id="bofqi")
            jsstring = da1.script.string

            p = re.compile(r'cid=\d+&')
            cid = p.findall(jsstring)[0][4:-1]
            print 'cid获取完成...'

        except Exception , e:
            print 'something serious happened  ->',
            print e
            exit()

        self.get_danmu(cid)
        
    def get_danmu(self,cid):
        danmu_url = "http://comment.bilibili.com/"+cid+".xml"

        data = self.gzip_url(danmu_url)
        print("弹幕页面 deflate解压完成...")
        # fd = open("danmu.xml",'w')
        # fd.write(data)
        # fd.close()

        soup = BeautifulSoup(data,'lxml')
        danmus = soup.find_all('d')
        fw = open('danmu.txt','w')
        print("写入弹幕ing...")
        for danmu in danmus:
            content = danmu.string

            attr = danmu['p'].split(',')
            t1 = attr[0] # 视频中的时间 
            t2 = attr[4] # 发布时间
            timestr = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(float(t2)))

            fw.write(content+'\t'+t1+'\t'+timestr+'\n')

        fw.close()
        print("写入完成...请查看danmu.txt")

        
def main():
    print "script_name:", sys.argv[0]
    b1 = BILI()
    print "av_number:",sys.argv[1],"parepering"
    url = r"http://www.bilibili.com/video/av"+sys.argv[1]
    b1.set_url(url)

if __name__ == '__main__':
    main()