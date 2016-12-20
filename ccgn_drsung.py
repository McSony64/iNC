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
  def __init__(self, url):
    super().__init__(url)
    self.myRevInit(url)
    self._dctUrlTitle = {}
    
    # for getting the url address : <a href="..."
    self._urlLeadingPtn  = '<a href="'
    self._urlTrailingPtn = '"'
    # for getting the subject title string ">...</a>
    self._titleLeadingPtn = '">'
    self._titleTrailingPtn = '</a>'
    '''
    <html>
    <title> 靈曆集光 </title>
    <meta http-equiv="Content-Type" content="text/html; charset=big5">

    lldt01.htm ... lldt14.htm
    list.htm, zx.htm lx.htm, xx.htm, sx.htm
    
    http://www.ccgn.nl/boeken02/lldt/list.htm
    
    '''
    self._fBase     = "/storage/emulated/0/Documents/ccgn_靈曆集光_"
    self._fExt      = ".txt"
    self._urlBase   = "http://www.ccgn.nl/boeken02/lljg/"
    
    
  def myRevInit(self, url):
    print("myRevInit(url[%s])" % (url))
    self.myRevinit(url)
        
    
  def getOnePage(self, url, fname):
    print("collecting %s ...\n\n" % (url))
    self.myRevInit(url)
    strTgt = self.collectBody()
    fd = open(fname,"w")
    fd.write(strTgt)
    self.printSep("#")
    print("saving file:%s ...\n\n" % (fname))
    fd.close()
    
        
    
    
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
    ###print("num links = %d" % (len(allLinks)))
    thIndx = 1
    for a in allLinks:
      ###print("[%d]th url = [%s]" % (thIndx, str(a)))
      strA = str(a)
      strUrl, strRes = self.nextUrl(strA)
      strTtl, strRes = self.titleAfterUrl(strRes)
      ###print("[%d]:: Url[%s], Title[%s]" % (thIndx, strUrl, strTtl))
      self._dctUrlTitle[strUrl] = strTtl.strip()
      thIndx += 1
      
  def removeWhiteSpaces(self, strSrc):
    lstTarget = ["\n", "\t", "\r", " "]
    for item in lstTarget:
      strSrc = strSrc.replace(item, "")
    return strSrc
      
  def collectEthicAdv(self):
        
    strTemp = self.getHtml()
    # check urlBase
    
    self.getAllLinks()   # get the urls and associated title/subject
    
    keys = self._dctUrlTitle.keys()
    for key in keys:
      ###print("Writing... dctUrlTitle[%s] = %s\n" % (key, self._dctUrlTitle[key]))

      # "http://www.ccgn.nl/boeken02/lljg/" + "f-lljg-401.htm"
      url = self._urlBase + key   
      # "/storage/emulated/0/Documents/ccgn_靈曆集光_" + " (3)在北平香山養病期間 " + ".txt"
      indxDot = key.find(".")
      fPrefix = key[:indxDot] + "_"
      fname = self._fBase + fPrefix + self._dctUrlTitle[key] + self._fExt
      fname = self.removeWhiteSpaces(fname)
      self.getOnePage(url, fname)
    
    
    

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
  ###trinity.getAllLinks()
  trinity.collectEthicAdv()
  
  ###strCS = trinity.getCharset()
  ###print("Charset = %s" % (strCS))

if __name__ == "__main__":
  main()








