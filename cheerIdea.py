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



class cheerfulIdeaScraper(CommonUrlSearch):
  '''
  http://www.cheeridea.asia/su101/2016-7-1/files/basic-html/
  http://www.cheeridea.asia/su101/2016-7-1/files/basic-html/page2.html
  http://www.cheeridea.asia/su101/2016-7-1/files/basic-html/page??.html
  http://www.cheeridea.asia/su101/2016-7-11/files/basic-html/
  http://www.cheeridea.asia/su101/2016-7-21/files/basic-html/
  http://www.cheeridea.asia/su101/2016-8all/files/basic-html/page??.html
  http://www.cheeridea.asia/su101/2016-9all/files/basic-html/page??.html
  July, 85 pages
  
  
  
  
  
  '''
  def __init__(self, url, enc = ""):
    super().__init__(url, enc)
    #self.myInit(url)
    self.dctCheerIdea = {}


  def myInit(self, url, enc = "", forcedZip = False):
    self.myinit(url, enc, forcedZip)
    
  def formatText(self, strSrc):
    print("formatText()")
    dctPtns0 = {}
    dctPtns0[0]  = "金句:"
    dctPtns0[1]  = "默想 / 應用:"
    dctPtns0[2]  = "祈禱 / 行動:"
    
    dctPtns1 ={}
    dctPtns1[0]  = ["一、", ")"]
    dctPtns1[1]  = ["二、", ")"]
    dctPtns1[2]  = ["三、", ")"]
    dctPtns1[3]  = ["一年聖經速讀", "\n"]
    #三、上帝的話語不落空(5-6 節)
    
    strTgt = strSrc
    ###print("00lenStrTgt = %d" % (len(strTgt)))
    for val in dctPtns0.values():
      ###print("val = %s" % (val))
      indxStart = strTgt.find(val)
      indxEnd   = indxStart + len(val)
      strFront  = strTgt[:indxStart]
      ###print("iStart[%d], iEnd[%d]" % (indxStart, indxEnd))
      ###print("99lenStrFront = %d" % (len(strFront)))
      strBack   = strTgt[indxEnd:]
      ###print("99lenStrEnd   = %d" % (len(strBack)))
      strMid    = "\n\n" + val + "\n\n"
      strTgt    = strFront + strMid + strBack
    ###print("01lenStrTgt = %d" % (len(strTgt)))
    ###print("xxx@@@@@@@@@@@@@@@@@@@@@@@@")
    ###print(strTgt)
    ###print("xxx@@@@@@@@@@@@@@@@@@@@@@@@")
     
    for val in dctPtns1.values():
      ptn0 = val[0]
      ptn1 = val[1]
      ###print("val = ", (val))
      indxStart = strTgt.find(ptn0)
      strTmp    = strTgt[indxStart:]
      indxEnd   = strTmp.find(ptn1)
      strMid    = "\n\n"+strTgt[indxStart:indxStart+indxEnd+1]+"\n\n"
      ###print("strMid = ", (strMid))
      strFront  = strTgt[:indxStart]
      ###print("iStart[%d], iEnd[%d]" % (indxStart, indxEnd))
      ###print("99lenStrFront = %d" % (len(strFront)))
      strBack   = strTgt[indxStart+indxEnd:]
      ###print("99lenStrEnd   = %d" % (len(strBack)))
      strTgt    = strFront + strMid + strBack
    ###print("02lenStrTgt = %d" % (len(strTgt)))

    ###input("Press a key to proceed.")

    return strTgt
 

  def collectInfoPages(self):
    print("collectInfoPages()")
    '''
    1st: Collect the base page
    2nd: Collect the base page + page2.html, page3,...,page10.html
    ...
    '''
    # get the base page
    strTemp = str(self.getSoup().pre)
    strTemp = self.removeAllTags(strTemp)
    strTemp = strTemp.replace("\n", "")+"\n"
    ###print("000@@@@@@@@@@@@@@@@@@@@@@@@")
    ###print(strTemp)
    ###print("000@@@@@@@@@@@@@@@@@@@@@@@@")
    strTemp = self.formatText(strTemp)
    ###print("333@@@@@@@@@@@@@@@@@@@@@@@@")
    ###print(strTemp)
    ###print("333@@@@@@@@@@@@@@@@@@@@@@@@")
    self.dctCheerIdea[1] = strTemp
    
    # start collecting page2.html, page3.html, etc.
    indxCurrent = 2
    lpCond = True
    print("self.getUrlBase(): %s" % (self.getUrlBase()))
    while lpCond:
      url = ""
      url = self.getUrlBase() + "page" + str(indxCurrent) + ".html"
      try:
        print("@@@@@@@ indxCurrent = %d" % (indxCurrent))
        print("@@@@@@@ url = %s <---" % (url))
       
        self.myinit(url, "", True)
      except urllib.error.HTTPError as err: 
        print("HTTP Error:: ", err.code)
        lpCond = False
        break
      
      objPre = self.getSoup().pre
      if objPre != None:
        strTemp = str(objPre)
        strTemp = self.removeAllTags(strTemp)
        strTemp = strTemp.replace("\n", "")+"\n"
        ###print("000@@@@@@@@@@@@@@@@@@@@@@@@")
        ###print(strTemp)
        ###print("000@@@@@@@@@@@@@@@@@@@@@@@@")
        strTemp = self.formatText(strTemp)
        ###print("333@@@@@@@@@@@@@@@@@@@@@@@@")
        ###print(strTemp)
        ###print("333@@@@@@@@@@@@@@@@@@@@@@@@")
        self.dctCheerIdea[indxCurrent] = strTemp
        indxCurrent += 1
        url = ""
      else:
        lpCond = False
        print("loop stops...")

    
    keys = self.dctCheerIdea.keys()
    ###print("lenKeys =%d" % (len(keys)))
    
    ###print("@@@@@@@@@@@@@@@@@@@@@@@@")
    ###input("Hello here here")
    for key in keys:
      strTgt = self.dctCheerIdea[key]
      print("@@@@@@@@@@@@@@@@@@@@@@@@")
      print("d[%d] == \n%s" % (key, strTgt))
    
    input("Hello there")
    
def main():
  url = "http://www.cheeridea.asia/su101/2016-7-1/files/basic-html/"
  cheerIdea = cheerfulIdeaScraper(url)
  
  cheerIdea.collectInfoPages()



if __name__=="__main__":
  main()