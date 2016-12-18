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
    
    
class CGNNtrinity(CommonUrlSearch):
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
    
        
  def collectTrinity(self):
    '''
    <html>
    <title>三一神論</title>
    <meta http-equiv="Content-Type" content="text/html; charset=big5">

    right.htm, sysl-x.htm, sysl-q.htm, wtjd.htm, 
    sysl-01.htm ... sysl-04.htm 
    
    http://www.ccgn.nl/boeken02/sysl/sysl-x.htm
  
    '''
    fBase     = "/storage/emulated/0/Documents/ccgn_三一神論_"
    fExt      = ".txt"
    urlBase   = "http://www.ccgn.nl/boeken02/sysl/"
    urlPrefix = "sysl-"
    urlSuffix = ".htm"
    for i in range(1,5):
      strIndx = str(i).zfill(2)
      url = urlBase + urlPrefix + strIndx + urlSuffix
      fname = fBase + strIndx + ".txt"
      self.getOnePage(url, fname)
      
    # get others: right.htm, sysl-x.htm, sysl-q.htm, wtjd.htm
    lstOthers = ["right", "sysl-x", "sysl-q", "wtjd"]
    for item in lstOthers:
      url   = urlBase + item + urlSuffix
      fname = fBase + item + fExt
      self.getOnePage(url, fname)


def main():
  url = "http://www.ccgn.nl/boeken02/sysl/sysl-x.htm"

  trinity = CGNNtrinity(url)  
  trinity.collectTrinity()


if __name__ == "__main__":
  main()
