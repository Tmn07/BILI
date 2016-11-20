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

import sys, getopt

# -----------
import argparse

reload(sys)
sys.setdefaultencoding("utf-8")


class BILI(object):
    def __init__(self, filename='danmu', parser='lxml'):
        self.filename = filename
        self.xml = False
        self.parser = parser

    def gzip_url(self, url):
        header = {
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Accept-Encoding': 'gzip',
            'Referer': 'http://www.bilibili.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:45.0) Gecko/20100101 Firefox/45.0'
        }
        request = urllib2.Request(url, headers=header)
        response = urllib2.urlopen(request)
        # gzip解压
        if response.info().get('Content-Encoding') == 'gzip':
            compresseddata = response.read()
            buf = StringIO(compresseddata)
            f = gzip.GzipFile(fileobj=buf)
            data = f.read()
        # deflate解压
        else:
            data = zlib.decompress(response.read(), -zlib.MAX_WBITS)
        return data

    def set_url(self, url):
        html = self.gzip_url(url)
        print '视频页面 gzip解压完成...'
        print (url)
        try:
            soup = BeautifulSoup(html,self.parser)
            da1 = soup.find('div', id="bofqi")
            jsstring = da1.script.string

            p = re.compile(r'cid=\d+&')
            cid = p.findall(jsstring)[0][4:-1]
            print 'cid获取完成...'
            self.get_danmu(cid)

        except Exception, e:
            print 'something serious happened  ->',
            print e
            # exit()

    def get_danmu(self, cid):
        danmu_url = "http://comment.bilibili.com/" + cid + ".xml"

        data = self.gzip_url(danmu_url)
        print("弹幕页面 deflate解压完成...")
        if self.xml:
            fd = open(self.filename + ".xml", 'w')
            fd.write(data)
            fd.close()
            print(self.filename + ".xml写入完成")

        soup = BeautifulSoup(data, self.parser)
        danmus = soup.find_all('d')
        fw = open(self.filename + '.txt', 'w')
        print("写入弹幕ing...")
        for danmu in danmus:
            content = str(danmu.string)

            attr = danmu['p'].split(',')
            t1 = str(attr[0])  # 视频中的时间
            t2 = attr[4]  # 发布时间
            timestr = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(t2)))

            fw.write(content + '\t' + t1 + '\t' + timestr + '\n')

        fw.close()
        print("写入完成...请查看%s.txt" % self.filename)


def main():
    parser = argparse.ArgumentParser(description='Welcome to BILI')
    parser.add_argument('-i', '--input', help='set the av_number to crawl')
    parser.add_argument('-o', '--output',  help='set the filename to store')

    parser.add_argument('-x','--xml', action='store_true', help='output as xml')
    parser.add_argument('-p', '--parser',help='default use lxml parser, but sometime wrong please use html.parser')
    parser.add_argument('-v','--version', action='store_true',help='show version')
    # parser.add_argument('-p', action='store_true') 
    args = parser.parse_args()

    if args.version == True:
        print("version 0.4")
        exit()

    b1 = BILI()
    # b1.setArgs(["parser","output","xml"],args)
    if args.parser:
        b1.parser = args.parser
    if args.output:
        b1.filename = args.output
    if args.xml:
        b1.xml = args.xml

    print "av_number:", str(args.input), "parepering"
    url = r"http://www.bilibili.com/video/av" + str(args.input)
    b1.set_url(url)


if __name__ == '__main__':
    main()
