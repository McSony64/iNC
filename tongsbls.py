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
import sys
from urlsearch import *

# 荷蘭華人基督教會
'''
url = "http://www.ccgn.nl/boeken02_e.html"

self.dctCCGN[“暗室之後“］   = "http://www.ccgn.nl/boekeseln02/aszh/knjy14.htm"
self.dctCCGN[“暗室之後續“］ = "http://www.ccgn.nl/boeken02/aszh/xj/knjy15.htm"

'''


class DrTongSBLS(CommonUrlSearch):
  def __init__(self, url, enc = ""):
    super().__init__(url, enc)
    self.myInit(url, "big5", True)
    self.dct = {}


  def myInit(self, url, enc = "", forcedZip = False):
    print("myInit()::url = %s", (url))
    self.myinit(url, enc, forcedZip)
    
  def getOne(self, url):
    self.myInit(url, "big5", True)
    strRes = self.collectBody()
    return strRes
    
  def collectBatch(self, iStart, iEnd, uBase, uExt, fBase, fExt):
    '''
    '''
    for item in range(iStart, iEnd):
      strI = str(item)
      url  = uBase + strI + uExt
      
      strRes = self.getOne(url)
      ###print(strI * 25)
      ###print(strTgt)
      fname = fBase + strI + fExt
      
      if strRes == "":
        print("item[%s]:: url error - content empty" % (item))
      else:
        fd = open(fname,"w")
        fd.write(strRes)
        self.printSep("#")
        print("file:%s collected." % (fname))
        fd.close()
      fname = ""

  def collectListBatch(self, lstUrls, uBase, uExt, fBase, fExt):
    '''
    '''
    for item in lstUrls:
      strI = str(item)
      url  = uBase + strI + uExt
      
      strRes = self.getOne(url)
      ###print(strI * 25)
      ###print(strTgt)
      fname = fBase + strI + fExt
      
      if strRes == "":
        print("item[%s]:: url error - content empty" % (item))
      else:
        fd = open(fname,"w")
        fd.write(strRes)
        self.printSep("#")
        print("file:%s collected." % (fname))
        fd.close()
      fname = ""

  def collectSermons(self):
    '''
    1-23, 26-43
    exceptions: 
    24a, 24b, 24c
    25a, 25b, 25c
    '''
    urlBase = "http://www.ccgn.nl/boeken02/xbls/"
    urlExt  = ".htm"
    fExt    = ".txt"
    fBase   = "/storage/emulated/0/Documents/xbls_" 
    numLectures = 43+1
    
    ###self.collectBatch(iStart, iEnd, uBase, uExt, fBase, fExt)
    ###self.collectBatch(1, 24, urlBase, urlExt, fBase, fExt)
    
    # self.collectListBatch(self, lstUrls, uBase, uExt, fBase, fExt)
    # get 24a, 24b, 24c, 25a, 25b, and 25c
    lstUrls = ["24a", "24b", "24c", "25a", "25b", "25c"]
    ###self.collectListBatch(lstUrls, urlBase, urlExt, fBase, fExt)
    
    self.collectBatch(26, numLectures, urlBase, urlExt, fBase, fExt)

  def removeLTBlankLines(self, lstLines, cntLeading, cntTrailing):
    # sanity check
    lenLines = len(lstLines)
    print("removeLTBlankLines(lenLines: %d, cntLeading: %d, cntTrailing: %d)" % (lenLines, cntLeading, cntTrailing))
    if lenLines < (cntLeading + cntTrailing):
      print("Error: fewer lines than requested to remove")
      return
      
    for l in range(cntLeading):
      line = lstLines[0]
      if line.isspace():
        lstLines.remove(line)
    for t in range(cntTrailing):
      line = lstLines.pop(len(lstLines)-1)
      if not line.isspace():
        print("Error: expected line is not empty at %d" % (len(lstLines)-1))
        
    return lstLines

  def processTrimFile(self, fname):
    lstLines      = []
    cntLeading    = 0
    cntLeadingMax = 0
    cntTrailing   = 0
    cntLines01    = 0
    cntLines02    = 0
    with open(fname) as f:
      lstLines   = f.readlines()   # read all lines 
      cntLines01 = len(lstLines)   # initial line cnt
      
      for line in lstLines:
        if cntLeading != -1:   # counting stops
          if line.isspace():
            cntLeading += 1
          else:   # finish counting leading empty lines
            cntLeadingMax = cntLeading
            cntLeading = -1
        else:   # start counting the trailing ones
          if not line.isspace():
            cntTrailing = 0
          else:
            cntTrailing += 1
      lstLines = self.removeLTBlankLines(lstLines, cntLeadingMax, cntTrailing)
      cntLines02 = len(lstLines)
      
      print("File changes:")
      print("-------"*5)
      print("original line cnt = %d" % (cntLines01))
      print("removed leading %d lines" % (cntLeadingMax))
      print("remved trailing %d lines" % (cntTrailing))
      print("modified line cnt = %d" % (cntLines02))
      print("======="*5+"\n\n")
    return lstLines
      
      

  def checkFile(self, fname):
    cntLeading    = 0
    cntLeadingMax = 0
    cntTrailing   = 0 
    with open(fname) as f:
      for line in f:
        if cntLeading != -1:   # counting stops
          if line.isspace():
            cntLeading += 1
          else:   # finish counting leading empty lines
            cntLeadingMax = cntLeading
            cntLeading = -1
        else:   # start counting the trailing ones
          if not line.isspace():
            cntTrailing = 0
          else:
            cntTrailing += 1
      return cntLeadingMax, cntTrailing
      
    
  def trimFiles(self, iStart, iEnd, fBase, fExt):
    for i in range(iStart, iEnd):
      ff = fBase + str(i) + fExt
      fg = fBase + "xyz" + str(i) + fExt


      lstRes  = self.processTrimFile(ff)
      
      fn = open(ff, "w")
      for line in lstRes:
        fn.write(line)
      fn.close()

      fn = open(ff)
      print(">>> %d lines written in " % (len(fn.readlines())))
      print(">>>>>>> %s <<<<<<<\n\n" % (str(i) + fExt))
      fn.close()



    
    
def main():
  '''
  hello there!
  '''
  url = "http://www.ccgn.nl/boeken02/xbls/1.htm"
  sblsScraper = DrTongSBLS(url)
  
  ###sblsScraper.collectSermons()
  fExt    = ".txt"
  fBase   = "/storage/emulated/0/Documents/xbls_" 

  '''
  f26     = fBase + "26" + fExt
  f27     = fBase + "27" + fExt
  lstRes  = sblsScraper.checkFile(f26)
  print("f26 info. ", lstRes)
  lstRes  = sblsScraper.checkFile(f27)
  print("f27 info. ", lstRes)
  '''      
  
  ###lstRes  = sblsScraper.processTrimFile(f27)
  ###print("f27 info : %d" % (len(lstRes)))
  sblsScraper.trimFiles(27, 44, fBase, fExt)  
  
  
if __name__ == "__main__":
  main()

