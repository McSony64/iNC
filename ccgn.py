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

# 荷蘭華人基督教會
url = "http://www.ccgn.nl/boeken02_e.html"

'''
self.dctCCGN[“暗室之後“］   = "http://www.ccgn.nl/boekeseln02/aszh/knjy14.htm"
self.dctCCGN[“暗室之後續“］ = "http://www.ccgn.nl/boeken02/aszh/xj/knjy15.htm"

'''


class CCGNScraper(CommonUrlSearch):
  '''
  基督徒處世生活詳盡指南 - Christan Living Guide
  http://www.ccgn.nl/boeken02/jdtcszn/chapter01.html
  01-87
  
  
  '''
  def __init__(self, url, enc = ""):
    super().__init__(url, enc)
    self.myInit(url, "big5", True)
    self.dct = {}


  def myInit(self, url, enc = "", forcedZip = False):
    print("myInit()::url = %s", (url))
    self.myinit(url, enc, forcedZip)
    
    
  def collectChristianLivingGuide(self):
    fBase = "/storage/emulated/0/Documents/ccgn_CLG"
    
    urlBase = "http://www.ccgn.nl/boeken02/jdtcszn/chapter"
    for i in range(1,88):
      strIndx = str(i).zfill(2)
      url = urlBase + strIndx + ".html"
      self.myInit(url, "big5", True)
      strTgt = self.collectBody()
      fname = fBase + strIndx + ".txt"
      fd = open(fname,"w")
      fd.write(strTgt)
      self.printSep("#")
      print("file:%s" % (strIndx))
      fd.close()
      
  '''
   鐵證待判：
   http://www.ccgn.nl/boeken02/tzdp/tzdp_qy.htm
   [<a href="tzdp_xy.htm">下一篇</a>]</td>
  '''
  def collectEvidenceVerdict(self, url):
    ptnTagA = '<a href="'
    
    fBase   = "/storage/emulated/0/Documents/ccgn_CLG"
    
    urlBase = "http://www.ccgn.nl/boeken02/tzdp/"
    urlPage = "tzdp_qy.htm"
    ptnNext = "下一篇"
         
    lpCond  = True
    while lpCond:
      if urlPage != "":
        indxDot = urlPage.find(".")
        fname   = urlPage[:indxDot]

        url = urlBase + urlPage
        try:
          self.myInit(url, "big5", True)
        except urllib.error.HTTPError as err:
          print("urllib.error.HTTPError::", err)
          break
           
        strTgt  = self.collectBody()
        strWtgt = self.collectBody(False)
        fname = fBase + fname + ".txt"
        fd = open(fname,"w")
        fd.write(strTgt)
        self.printSep("#")
        print("file:%s" % (fname))
        fd.close()
        fname = ""
        # Collect next urlPage
        indxNext = strWtgt.find(ptnNext)
        if indxNext == -1:
          urlPage = ""
        else:
          strTemp   = strWtgt[:indxNext]
          indxPtnA  = strTemp.rfind(ptnTagA)
          strSearch = strWtgt[indxPtnA:indxNext]
          print("strTemp :: %s" % (strTemp))
          print("urlTgt:%s" % (strSearch))
          print("indxPtnA[%d]:indxNext[%d]" % (indxPtnA, indxNext))
          indxTail  = strSearch.rfind('">')
          strUrlTgt = strSearch[len(ptnTagA):indxTail]
          print("strUrlTgt:%s" % (strUrlTgt))
          urlPage   = strUrlTgt
          input("Hit a key to proceed")

  def getEVone(self, url, upperTags = False, forceZip = True):
    strTgt = ""
    try:
      self.myInit(url, "big5", forceZip)
      strTgt  = self.collectBody(upperTags, forceZip)
    except urllib.error.HTTPError as err:
      print("urllib.error.HTTPError::", err)

    ###strWtgt = self.collectBody(False)        
    return strTgt

  def collectSet(self):
    lstSet  = ["12", "my", "jp", "jj", "ck"]
    urlBase = "http://www.ccgn.nl/boeken02/tzdp/"
    urlPage = "tzdp_"
    urlExt  = ".htm"
    fBase   = "/storage/emulated/0/Documents/ccgn_" 
    
    for item in lstSet:
      fname  = fBase + urlPage + item + ".txt"
      url    = urlBase + urlPage + item + urlExt
      strRes = self.getEVone(url)
      
      if strRes == "":
        print("item[%s]:: url error - content empty" % (item))
      else:
        '''
        fd = open(fname,"w")
        IOError: [Errno 2] No such file or 
        directory: '/storage/emulated/0/Documents/ccgn_/storage/emulated/0/Documents/ccgn_tzdp_11.txt.txt'
        '''
        fd = open(fname,"w")
        fd.write(strRes)
        self.printSep("#")
        print("file:%s collected." % (fname))
        fd.close()
      fname = ""
      
  def getRevelationStudy(self):   
    '''
    http://www.ccgn.nl/boeken02/qisilu/big5/r.htm
    0-39.htm
    '''
    urlBase = "http://www.ccgn.nl/boeken02/qisilu/big5/"
    urlExt  = ".htm"
    fExt    = ".txt"
    fBase   = "/storage/emulated/0/Documents/qisilu_" 

    for item in range(40):
      strI = str(item)
      url  = urlBase + strI + urlExt
      
      strRes = self.getEVone(url)
      ###print(strI * 25)
      ###print(strTgt)
      fname = fBase + strI + fExt
      
      
      if strRes == "":
        print("item[%s]:: url error - content empty" % (item))
      else:
        '''
        
        '''
        fd = open(fname,"w")
        fd.write(strRes)
        self.printSep("#")
        print("file:%s collected." % (fname))
        fd.close()
      fname = ""
      
  def collectMEancestry(self):
    urlBase = "http://www.ccgn.nl/boeken02/zdzylsz/chapter"
    urlExt  = ".html"
    numChs  = ""
    
  def collectPilgrimsProgress(self, write2file = False):
    '''
    pilg-tl.htm, pilg-intr.ntm, pilg-pf, 
    pilg-01.htm - pilg21.htm
    '''
    
    urlBase = "http://www.ccgn.nl/boeken02/tllc/pilg-"    
    urlExt  = ".htm"
    fExt    = ".txt"
    fBase   = "/storage/emulated/0/Documents/pilg-" 

    for item in range(1, 3):  #2):
      strI = str(item).zfill(2)
      url  = urlBase + strI + urlExt
      
      strRes = self.getEVone(url, True)
      ###print(strI * 25)
      ###print(strTgt)
      fname = fBase + strI + fExt
      
      
      if strRes == "":
        print("item[%s]:: url error - content empty" % (item))
      else:
        '''
        
        '''
        if write2file:
          fd = open(fname,"w")
          fd.write(strRes)
          fd.close()
        self.printSep("#")
        print("file:%s collected." % (fname))
        
      fname = ""
             

def main():
  url = "http://www.ccgn.nl/boeken02/jdtcszn/chapter01.html"  
  myScraper = CCGNScraper(url)
  ##myScraper.collectChristianLivingGuide()
  
  url = "http://www.ccgn.nl/boeken02/tzdp/tzdp_qy.htm"
  ###myScraper.collectEvidenceVerdict(url)
  ###myScraper.collectSet()
  ###myScraper.getRevelationStudy()
  myScraper.collectPilgrimsProgress()

if __name__ == "__main__":
  main()