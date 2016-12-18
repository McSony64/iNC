# -*- coding: utf-8 -*-
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


class CGNNapology(CommonUrlSearch):
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

    
  def collectApologeticsGuide(self):
    '''
    <html>
    <head>
    <title>護教手冊</title>
    <meta http-equiv="Content-Type" content="text/html; charset=big5">
    <style type="text/css">
    </style>
    <base target="_self"></head>

    chapter01.html ... chapter15.html
    index.html

    '''
    fBase = "/storage/emulated/0/Documents/ccgn_護教手冊_"    
    urlBase = "http://www.ccgn.nl/boeken02/hujiaosouce/"
    for i in range(1,16):
      strIndx = str(i).zfill(2)
      url = urlBase + "chapter" + strIndx + ".html"
      fname = fBase + strIndx + ".txt"

      self.getOnePage(url, fname)
      '''
      self.myInit(url, "big5", True)
      strTgt = self.collectBody()
      fd = open(fname,"w")
      fd.write(strTgt)
      self.printSep("#")

      fd.close()
      '''
    

def main():
  url = " http://www.ccgn.nl/boeken02/hujiaosouce/index.html"
  ccgnApo = CGNNapology(url)
  ###ccgnApo.collectApologeticsGuide()
  
  # cellect index.html
  urlBase = "http://www.ccgn.nl/boeken02/hujiaosouce/"
  url     = urlBase + "index.html"
  fBase   = "/storage/emulated/0/Documents/ccgn_護教手冊_"    
  fname   = fBase + "index.txt"
  ccgnApo.getOnePage(url, fname)  
  
if __name__ == "__main__":
  main()
