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

from xml.dom.minidom import parse
import xml.dom.minidom
  
import time

import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

class BILI(object):
    #或者接收url
    def __init__(self):
        pass
    def gzip_url(self,url):
#        request = urllib2.Request(url)
#        request.add_header('Accept-encoding', 'gzip')
#        response = urllib2.urlopen(request)
        response = urllib2.urlopen(url)
        if response.info().get('Content-Encoding') == 'gzip':
            compresseddata = response.read()
            buf = StringIO(compresseddata)
            f = gzip.GzipFile(fileobj=buf)
            data = f.read()
        else:
            data = zlib.decompress(response.read(),-zlib.MAX_WBITS)
        return data

    def set_url(self,url):
        html = self.gzip_url(url)
        soup = BeautifulSoup(html,"html.parser", from_encoding="utf-8")   
        try:
            
            da1 = soup.find('div',id="bofqi")
            
            jsstring = unicode(da1.script.string)
            
            ####之后用正则改。。慢？
            cidstring = jsstring.split("\"")[3]
    #        print cidstring
            cid = int(cidstring[4])
    
            for i in range(5,len(cidstring)):
                char = cidstring[i]
                if char.isdigit():
                    cid = cid*10+int(char)
                else:
                    break
            self.cid = str(cid)
            return cid
        except Exception , e:
            print 'something serious happened  ->',
            print e
            exit()
        
    def get_danmu(self):
        ###解析XML。。。先不做了。。
        
        danmu_url = "http://comment.bilibili.com/"+self.cid+".xml"
        
        data = self.gzip_url(danmu_url)
#        print data
        
        fd = open("danmu.xml",'w')
        fd.write(data)        
        fd.close()
        print "XML has been write down from internet"
        
        root = xml.dom.minidom.parse("danmu.xml")
        ds = root.getElementsByTagName('d')
        fw = open('danmu.txt','w')
        print "XML reading.."
        for i in range(len(ds)):
            try:
                                
#                print ds[i].firstChild.data,
                fw.write(ds[i].firstChild.data)
                fw.write('\t')
                timelist = ds[i].getAttribute("p").split(',')
#                x = time.localtime(1317091800.0)
                ###改善？？
                x = time.localtime(float(timelist[4]))
                timestr = time.strftime('%Y-%m-%d %H:%M:%S',x)
#                print timelist[0],timestr
                fw.write(timelist[0])
                fw.write('\t')
                fw.write(timestr)
                fw.write('\n')
            except Exception , e:
                fw.write('\n')
                print 'something wrong happened but not serious ->',
                print e
        fw.close()
        
#        print danmu_url



#for i in range(1, len(sys.argv)):

#    print "参数", i, sys.argv[i]

print "script_name:", sys.argv[0]


b1 = BILI()
#url = r"http://www.bilibili.com/video/av4294705/"

print "av_number:",sys.argv[1],"parepering"
url = r"http://www.bilibili.com/video/av"+sys.argv[1]

b1.set_url(url)
print "cid_completed"
b1.get_danmu()
print "Completed.And resource in danmu.xml,danmu.txt"
