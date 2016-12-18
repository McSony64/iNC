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
    
    
class CGNNhomeLoveHouse(CommonUrlSearch):
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
    
        
  def collectHloveH(self):
    '''
    <html>
    <title> 聖經如此說</title>
    <meta http-equiv="Content-Type" content="text/html; charset=big5">

    chap1.htm ... chap16.htm
    
    http://www.ccgn.nl/boeken02/jsazw/index.htm
  
    '''
    fBase     = "/storage/emulated/0/Documents/ccgn_聖經如此說_"
    fExt      = ".txt"
    urlBase   = " http://www.ccgn.nl/boeken02/jsazw/"
    urlPrefix = "jt"
    urlSuffix = ".htm"
    
    for i in range(1,8):
      strIndx = str(i).zfill(2)
      url = urlBase + urlPrefix + strIndx + urlSuffix
      fname = fBase + strIndx + fExt
      self.getOnePage(url, fname)
     
    # get others: if any
    url = urlBase + "index" + urlSuffix
    fname = fBase + "index" + fExt
    self.getOnePage(url, fname)

def main():
  '''
  http://www.ccgn.nl/boeken02/jsazw/index.htm
  '''
  url = "http://www.ccgn.nl/boeken02/jsazw/index.htm"

  trinity = CGNNhomeLoveHouse(url)  
  trinity.collectHloveH()
  

if __name__ == "__main__":
  main()








