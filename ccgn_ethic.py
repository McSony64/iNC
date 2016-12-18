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
    
    
class CGNNethic(CommonUrlSearch):
  def __init__(self, url, enc = ""):
    super().__init__(url, enc)
    self.myInit(url, "utf-8", True)
    self.dct = {}
    
    
  def myInit(self, url, enc = "", forcedZip = False):
    print("myInit(url[%s])" % (url))
    self.myinit(url, enc, forcedZip)
        
  def getOnePage(self, url, fname):
    print("collecting %s ...\n\n" % (url))
    self.myInit(url, "utf-8", True)
    strTgt = self.collectBody()
    fd = open(fname,"w")
    fd.write(strTgt)
    self.printSep("#")
    print("saving file:%s ...\n\n" % (fname))
    fd.close()
    
        
  def collectEthic(self):
    '''
    <html>
    <title> 跨世紀倫理地圖 </title>
    <meta http-equiv="Content-Type" content="text/html; charset=big5">

    lldt01.htm ... lldt14.htm
    list.htm, zx.htm lx.htm, xx.htm, sx.htm
    
    http://www.ccgn.nl/boeken02/lldt/list.htm
    
    '''
    fBase     = "/storage/emulated/0/Documents/ccgn_跨世紀倫理地圖_"
    fExt      = ".txt"
    urlBase   = " http://www.ccgn.nl/boeken02/lldt/"
    urlPrefix = "lldt"
    urlSuffix = ".htm"
    lstOthers = ["list", "zx", "lx", "xx", "sx"]
    
    for i in range(1,14):
      strIndx = str(i).zfill(2)
      url = urlBase + urlPrefix + strIndx + urlSuffix
      fname = fBase + strIndx + fExt
      self.getOnePage(url, fname)
    
    # get others: if any
    for item in lstOthers:
      url = urlBase + item + urlSuffix
      fname = fBase + item + fExt
      self.getOnePage(url, fname)

def main():
  '''
  
  '''
  url = "http://www.ccgn.nl/boeken02/lldt/list.htm"

  trinity = CGNNethic(url)  
  trinity.collectEthic()
  

if __name__ == "__main__":
  main()








