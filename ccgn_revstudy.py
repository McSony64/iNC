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
    
    
class CGNNrevStudy(CommonUrlSearch):
  def __init__(self, url, enc = ""):
    super().__init__(url, enc)
    self.myInit(url, "big5", True)
    self.dct = {}
    
    
  def myInit(self, url, enc = "", forcedZip = False):
    print("myInit()::url = %s", (url))
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
    
        
  def collectRevStudy(self):
    '''
    <html>
    <head>
    <title>護教手冊</title>
    <meta http-equiv="Content-Type" content="text/html; charset=big5">
    <style type="text/css">
    </style>
    <base target="_self"></head>
  
    chapter1.htm ... chapter39.htm
    r.html
  
    '''
    fBase = "/storage/emulated/0/Documents/ccgn_啟示錄研究_"    
    urlBase = "http://www.ccgn.nl/boeken02/qisilu/big5/"
    for i in range(1,40):
      strIndx = str(i)
      url = urlBase + strIndx + ".htm"
      fname = fBase + strIndx + ".txt"

      self.getOnePage(url, fname)


def main():
  url = "http://www.ccgn.nl/boeken02/qisilu/big5/r.htm"

  '''
  0.html .. 39.html
  '''
  revStudy = CGNNrevStudy(url)  
  revStudy.collectRevStudy()
  # get index page
  fBase = "/storage/emulated/0/Documents/ccgn_啟示錄研究_" 
  fname = fBase + "index.txt"   
  revStudy.getOnePage(url, fname)


if __name__ == "__main__":
  main()
