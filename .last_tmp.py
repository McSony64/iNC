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
    <title> 靈曆集光 </title>
    <meta http-equiv="Content-Type" content="text/html; charset=big5">

    lldt01.htm ... lldt14.htm
    list.htm, zx.htm lx.htm, xx.htm, sx.htm
    
    http://www.ccgn.nl/boeken02/lldt/list.htm
    
    '''
    fBase     = "/storage/emulated/0/Documents/ccgn_靈曆集光_"
    fExt      = ".txt"
    urlBase   = "http://www.ccgn.nl/boeken02/lljg/"
    urlPrefix = "lldt"
    urlSuffix = ".htm"
    lstOthers = ["pre1", "int", "thank"]
    
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
      
  def nextUrl(self, strSrc):
    strTemp = strSrc
    indxLead  = 0
    indxTrail = 0
    indxLead = strTemp.find( self._urlLeadingPtn )
    if indxLead == -1:
      return "", strTemp  # not found
    else:
      strTemp1 = strTemp[ indxLead + len( self._urlLeadingPtn ):]
      indxTrail = strTemp1.find( self._urlTrailingPtn )
      if indxTrail != -1:   # found
        strUrl  = strTemp1[ :indxTrail ]
        strTemp = strTemp1[ indxTrail: ]
        return strUrl, strTemp
      else:
        return "", strTemp  # not found
        
  def titleAfterUrl(self, strSrc):
    '''
    Must called after nextUrl()
    '''
    
    strTemp = strSrc
    indxLead  = 0
    indxTrail = 0
    indxLead = strTemp.find( self._titleLeadingPtn )
    if indxLead == -1:
      return "", strTemp  # not found
    else:
      strTemp1 = strTemp[ indxLead + len( self. _titleLeadingPtn ):]
      indxTrail = strTemp1.find( self. _titleTrailingPtn )
      if indxTrail != -1:   # found
        strUrl  = strTemp1[ :indxTrail ]
        strTemp = strTemp1[ indxTrail: ]
        return strUrl, strTemp
      else:
        return "", strTemp  # not found    
    
  def getAllLinks(self):
    allLinks = self.getSoup().find_all('a')    
    print("num links = %d" % (len(allLinks)))
    thIndx = 1
    for a in allLinks:
      print("[%d]th url = [%s]" % (thIndx, str(a)))
      thIndx += 1
      
  def collectEthicAdv(self):
    # for getting the url address : <a href="..."
    self._urlLeadingPtn  = '<a href="'
    self._urlTrailingPtn = '"'
    # for getting the subject title string ">...</a>
    self._titleLeadingPtn = '">'
    self._titleTrailingPtn = '</a>'
    
    strTemp = self.getHtml()
    # check urlBase
    
    moreSearch = True
    while moreSearch:
      url, strTemp = self.nextUrl( strTemp )
      if url == "":
        print("done: no more urls found")
        moreSearch = False
      else:
        print("\n\nSearched url[%s]\n" % (url))
        
      print("->->->->=>=>=>remaining str [%s]:::>>>%d<<<" % (strTemp[:50], len(strTemp)))
        
      ttl, strTemp = self.titleAfterUrl( strTemp )
      if ttl == "":
        print("done: no more titles found")
        moreSearch = False
      else:
        print("\nSearched title[%s]\n\n" % (ttl))
     
    
    
    
    

def main():
  '''
  www.ccgn.nl/boeken02/lljg/right.htm
  f-lljg-101.htm
  pre1.htm, int.htm, thank.htm
  101.htm - 104.htm
  201.htm - 211.htm
  301.htm - 312.htm
  401.htm - 411.htm
  501.htm - 509.htm
  601.htm - 605.htm
  
  '''
  url = "http://www.ccgn.nl/boeken02/lljg/right.htm"

  trinity = CGNNethic(url)  
  #trinity.collectEthicAdv()
  trinity.getAllLinks()
  
  ###strCS = trinity.getCharset()
  ###print("Charset = %s" % (strCS))

if __name__ == "__main__":
  main()