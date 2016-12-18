# - coding: utf-8 -*-
import urllib
import urllib.request as request
import urllib.parse as parse
import re 
from bs4 import BeautifulSoup 
from datetime import datetime 
import gzip
import io
import zlib
import unicodedata
import time
from urlsearch import *
    
    
class CGNNtoughQuestions(CommonUrlSearch):
  def __init__(self, url, enc = ""):
    super().__init__(url, enc)
    self.myInit(url, "big5", True)
    self.dct = {}
    
    
  def myInit(self, url, enc = "", forcedZip = False):
    print("myInit(url[%s])" % (url))
    self.myinit(url, enc, forcedZip)
        
  def getOnePage(self, url, fname):
    print("collecting %s ...\n\n" % (url))
    self.myInit(url, "big5", True)
    strTgt = self.collectBody()
    fd = open(fname,"w")
    fd.write(strTgt)
    self.printSep("#")
    print("saving file:%s ...\n\n" % (fname))
    fd.close()
    
        
  def collectToughQuestions(self):
    '''
    <html>
    <title> 聖經難題彙編 </title>
    <meta http-equiv="Content-Type" content="text/html; charset=big5">

    chapter01.html ... chapter60.html
    
    http://www.ccgn.nl/boeken02/sjnthb/list.html
    http://www.ccgn.nl/boeken02/sjnthb/chapter01.html
  
    '''
    fBase     = "/storage/emulated/0/Documents/ccgn_聖經難題彙編_"
    fExt      = ".txt"
    urlBase   = "http://www.ccgn.nl/boeken02/sjnthb/"
    urlPrefix = "chapter"
    urlSuffix = ".html"
    '''
    for i in range(1,61):
      if i != 6:
        strIndx = str(i).zfill(2)
        url = urlBase + urlPrefix + strIndx + urlSuffix
        fname = fBase + strIndx + ".txt"
        self.getOnePage(url, fname)
    '''
      
    # get others: right.htm, sysl-x.htm, sysl-q.htm, wtjd.htm
    lstOthers = ["list", "chapter06.1", "chapter06.2", "chapter60" ]
    for item in lstOthers:
      url   = urlBase + item + urlSuffix
      fname = fBase + item + fExt
      self.getOnePage(url, fname)


def main():
  url = "http://www.ccgn.nl/boeken02/sjnthb/list.html"

  trinity = CGNNtoughQuestions(url)  
  ###trinity.collectToughQuestions()
  fname     = "/storage/emulated/0/Documents/ccgn_聖經難題彙編_60.txt"
  url       = "http://www.ccgn.nl/boeken02/sjnthb/chapter60.html"
  
  trinity.getOnePage(url, fname)

if __name__ == "__main__":
  main()
