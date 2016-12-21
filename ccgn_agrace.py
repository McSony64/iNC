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
gDebug = True    
    
class CGNNabudantGrace(CommonUrlSearch):
  def __init__(self, url):
    super().__init__(url)
    self.myRevInit(url)
    self._dctUrlSubject = {}
    
    # for getting the url address : <a href="..."
    self._urlLeadingPtn  = '<a href="'
    self._urlTrailingPtn = '"'
    # for getting the subject title string ">...</a>
    self._subjectLeadingPtn = '">'
    self._subjectTrailingPtn = '</a>'
    self._title = ""
    '''
    <html>
    <TITLE>豐盛的恩典</TITLE>

    http://www.ccgn.nl/boeken02/fsed/index.htm
    
    '''
    self._fBase     = "/storage/emulated/0/Documents/ccgn_"
    self._fExt      = ".txt"
    self._urlBase   = "http://www.ccgn.nl/boeken02/fsed/"
    
    
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
        
  def subjectAfterUrl(self, strSrc):
    '''
    Must called after nextUrl()
    '''
    
    strTemp = strSrc
    indxLead  = 0
    indxTrail = 0
    indxLead = strTemp.find( self._subjectLeadingPtn )
    if indxLead == -1:
      return "", strTemp  # not found
    else:
      strTemp1 = strTemp[ indxLead + len( self._subjectLeadingPtn ):]
      indxTrail = strTemp1.find( self._subjectTrailingPtn )
      if indxTrail != -1:   # found
        strUrl  = strTemp1[ :indxTrail ]
        strTemp = strTemp1[ indxTrail: ]
        return strUrl, strTemp
      else:
        return "", strTemp  # not found    
    
  def getAllLinks(self):
    allLinks = self.getSoup().find_all('a')
    if gDebug:
      print("num links = %d" % (len(allLinks)))
    thIndx = 1
    for a in allLinks:
      strA = str(a)
      strA = self.removeWhiteSpaces(strA, ["\n", "\t"])
      if gDebug:
        print("[[[%dth]]] url = [%s]" % (thIndx, strA))
      strUrl, strRes = self.nextUrl(strA)
      strSub, strRes = self.subjectAfterUrl(strRes)
      strSub = self.removeWhiteSpaces(strSub)
      if gDebug:
        print("[[[%d]]]:: Url[%s], Subject[%s]" % (thIndx, strUrl, strSub))
      self._dctUrlSubject[strUrl] = strSub
      thIndx += 1
      
  def removeWhiteSpaces(self, strSrc, lst2remove = []):
    if lst2remove == []:
      lstTarget = ["\n", "\t", "\r", " "]
      for item in lstTarget:
        strSrc = strSrc.replace(item, "")
    else:
      for item in lst2remove:
        strSrc = strSrc.replace(item, "")
    return strSrc
      
  def collectAdv(self, lstExclude = []):
    gDebug = False
    print("------- collectAdv() -------")
    self._title = self.getTitle()    
    self.getAllLinks()   # get the urls and associated title/subject
    
    keys = self._dctUrlSubject.keys()
    for key in keys:
      value = self._dctUrlSubject[key]
      '''
      print("value[%s]" % (value))
      if value == "返回":
        print("found found 返回:::", lstExclude)
        if value in lstExclude:
          print("Yes Yes in lstExclude[%s]" % (value))
      '''
      if not(value in lstExclude):
        ###print("Writing... dctUrlSubject[%s] = %s\n" % (key, self._dctUrlSubject[key]))

        # "http://www.ccgn.nl/boeken02/lljg/" + "f-lljg-401.htm"
        url = self._urlBase + key   
        # "/storage/emulated/0/Documents/ccgn_" + strTitle + "_" + strSubject + ".txt"
        indxDot = key.find(".")
        fPrefix = key[:indxDot] + "_"
        fname = self._fBase + self._title + "_" + fPrefix + self._dctUrlSubject[key] + self._fExt
        fname = self.removeWhiteSpaces(fname)
        if gDebug:
          print("url[%s] ===> fname[%s]" % (url, fname))    
        else:
          self.getOnePage(url, fname)
      else:
        print("!!!!!!!>>> value[%s] in lstExclude[]" % (value))
        continue
    
    

def main():
  '''
  '''
  url = "http://www.ccgn.nl/boeken02/fsed/index.htm"

  aGrace = CGNNabudantGrace(url)  
  ###aGrace.getAllLinks()
  lstExclude = ["返回"]
  aGrace.collectAdv(lstExclude)
  
  strCS = aGrace.getCharset()
  print("Charset = %s" % (strCS))
  aGrace.getTitle()

if __name__ == "__main__":
  main()
