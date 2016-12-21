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

gDebug = True    # True
  
  
class CommonUrlSearch(object):
  '''
  For websotes like YNetNews ("http://www.ynetnews.com/home/0,7340,L-3083,00.html")
  User_Agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
  url = "http://www.google.com/search?hl=en&safe=off&q=Monkey"
  headers={'User-Agent':user_agent,} 
  request=urllib2.Request(url,None,headers) #The assembled request 
  response = urllib2.urlopen(request) data = response.read() # The data u need
  
  '''
  

  def __init__(self, url):
    """ Scrape the given url for match schedule """ 

    self._headers = {#'Accept':'text/css,*/*;q=0.1', 
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.3', 
    'Accept-Encoding':'gzip,deflate,sdch', 
    'Accept-Language':'en-US,en;q=0.8', 
    #'User-Agent':'Mozilla/5 (Solaris 10) Gecko'} 
    'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'}

    
    self.myRevinit(url)
    
    # html codes
    self._ptnHtmlCode = '&#[0-9]+[;]'
    self._reHtmlCode  = re.compile(self._ptnHtmlCode)
    self._ptnPunct    = '[><}{)(.,"]+'
    self._rePunct     = re.compile(self._ptnPunct)
    self._ptnFormat   = '&[a-zA-Z;]+'
    self._reFormat    = re.compile(self._ptnFormat)


  def getSoup(self):
    return self._soup
    
  def getHtml(self):
    return self._html
    
  def getUrl(self):
    return self._url

  def getCharset(self):
    '''
    This has to be called after the soup object is created.
    
    It returns the expected charset string e.g., "big5", "utf-8", etc.
    
    <meta http-equiv="Content-Type" content="text/html; charset=big5">
    
    methods:
    (1) string find s.find(...)
    '''
    strCharsetPtn0 = ' charset='
    strCharsetPtn1 = '"'
    lenCharsetPtn0 = len(strCharsetPtn0)
    lenCharsetPtn1 = len(strCharsetPtn1)
    
    blkHeader  = str(self.getSoup().head.prettify())
    print("blkHeader: \n%s\n\n" % (blkHeader))
            
    indxPtn0   = blkHeader.find(strCharsetPtn0)
    strRemain0 = blkHeader[indxPtn0 + lenCharsetPtn0:]
    indxPtn1   = strRemain0.find(strCharsetPtn1)
    indxAnchorPtn0 = indxPtn0 + lenCharsetPtn0
    indxAnchorPtn1 = indxAnchorPtn0 + indxPtn1
    strCharset     = blkHeader[indxAnchorPtn0:indxAnchorPtn1]

    '''
    print("indxPtn0[%d]       = > charset< loc." % (indxPtn0))
    print("indxPtn1[%d]       = strRemain0 searched loc. for strCharsetPt1" % (indxPtn1))
    print("indxAnchorPtn0[%d] = leading index of target strCharset + len" % (indxAnchorPtn0))
    print("indxAnchorPtn1[%d] = indxAnchorPtn0 + indxPtn1" % ( indxAnchorPtn1))
    '''

    print("\n\n    ~~~~~~~ Searched Charset = >>>%s<<< ~~~~~~~" % (strCharset))
    
    return strCharset

  def getTitle(self):
    strTitle = str(self.getSoup().title)
    self._leadingTitlePtn  = "<title>"
    self._trailingTitlePtn = "</title>"
    indxLead  = strTitle.find(self._leadingTitlePtn) + len(self._leadingTitlePtn)
    indxTrail = strTitle.find(self._trailingTitlePtn)
    strTitle  = strTitle[indxLead:indxTrail]
    print("Page title[%s]" % (strTitle))

    return strTitle
    
  def invalidTitle(self, strTitle):
    self._rePunct.search("")
    
  def myRevinit(self, url, enc = "", forcedZip = False):
    print("myRevinit()::myRevinit()")
    self._url = url
    req = request.Request(url, None, self._headers)
    req.add_header('Accept-encoding', 'gzip')
    response = request.urlopen(req)
    html = response.read()
    
    #print(">>>>>>><<<<<<<\n response.header = \n\n%s\n\n >>>>>>><<<<<<<\n" % (response.headers))  #.getparam('charset')))

    if response.info().get('Content-Encoding') == 'gzip': 
      print("ALERT :: URL PAGE COMPRESSED!!!\n%s" % (url))
      gzipped = True
    else:
      gzipped = False

    #print("gzipped::", gzipped)
    if gzipped:
      html = zlib.decompress(html, 16+zlib.MAX_WBITS)
    ###print(html)
    
    # Try to get Charset here
    charset = ""
    self._soup = BeautifulSoup(html, "html.parser")
    charset = self.getCharset()
    print("\n\n~~~ HERE HERE ~~~ >>>%s<<<\n\n" % (charset))
    
    '''
    if enc == "":
      print("### utf-8 ###")
      self._html = html.decode("utf-8", "ignore")
    else:
    '''
    if charset != "":
      print("enc = %s" % (enc))
      print("WARNING!!!WARNING!!! \ndetected charset is [%s] and forced set to <%s>." % (charset, enc))
      print("Overwrite user's choice and set to <%s>\n\n" % (charset))
      if charset in ["utf-8", "utf8", "UTF8", "UTF-8"]:
        self._html = html   # avoid double decoding by BS
      else:
        self._html = html.decode(charset, "ignore")
    else:
      print("@@@@@@@ ALERT @@@@@@")
      print("Charset not found\n\n")

    print("@@@@@@@ myRevinit @@@@@@@ %s" % (url))
    ###print(self._html)
    self._soup = BeautifulSoup(self._html, "html.parser")
    
    '''
    strMark = "¥¥¥"*6 + " myinit()..print _soup.body " + "¥¥¥"*6    
    print(strMark)
    print(strMark)
    print(self._soup.body.prettify())
    print(strMark)
    print(strMark)
    '''

    
  def collectBody(self, upperTags = False, stripTags = True):
    '''
    dependent on myinit()
    
    '''
    print("collectBody()::collectBody()")
    if upperTags:
      body = self.getSoup().BODY
      print("get self.getSoup().BODY")
    else:
      body = self.getSoup().body
      print("get self.getSoup().body")
    self.printSep("€")
    strBody = str(body)
    ###print("BBB ::: %s" % (strBody))
    if upperTags:
      strBody = strBody.replace("<BR>","\n")
    else:
      strBody = strBody.replace("<br>","\n")
    if stripTags:
      strBody = self.removeAllTags(strBody)
    ###print(strBody)
    return strBody

  def printSep(self, strPtn):
    print(strPtn*25)
      
  def removeAllTags(self, strSrc):
    print("removeAllTags()::removeAllTags()")
    # remove <…> 
    # s[start:end+1] = "<…>"
    tagStart  = '<'
    tagEnd    = '>'
    strTemp   = str(strSrc)
    indxStart = -1
    indxEnd   = -1
    cntLoop   = 1
    strTemp   = strTemp.replace("<p>",  "\n")
    strTemp   = strTemp.replace("</p>", "\n")
    
    # remove script code blocks
    moreScript = True
    sStart     = "<script>"
    sEnd       = "</script>"
    while moreScript:
      indxStart = strTemp.find(sStart)
      indxEnd   = strTemp.find(sEnd)
      if indxStart == -1 or indxEnd == -1:
        print("No more scripts")
        moreScript = False
        break
      else:
        strFront = strTemp[:indxStart]
        strBack  = strTemp[indxEnd+len(sEnd):]
        strRem   = strTemp[indxStart+len(sStart): indxEnd]
        strTemp  = strFront + strBack
        print("iS[%d], iE[%d], REMOVE:%s" % (indxStart, indxEnd, strRem))
        
    #print("SSS:::%s" % (strTemp))
    #input("A0:Enter any key to proceed")
    lpCondition = True
    while lpCondition:
      lnStrTemp = len(strTemp)
      indxStart = strTemp.find(tagStart)
      #print("------------------\n")
      #print(">>>--%s\n" % (strTemp))
      if indxStart != -1:  # found
        indxEnd = strTemp.find(tagEnd)
        ###print("222:: indxStart[%d] indxEnd[%d]" % (indxStart, indxEnd))
        
        '''
        indxOne = indxStart -5
        if indxOne < 0:
          indxOne = 0
        indxTwo = indxStart +5
        neighbor1 = strTemp[indxOne:indxTwo]
        
        indxOne = indxEnd -5
        indxTwo = indxEnd +5        
        neighbor2 = strTemp[indxOne:indxTwo]        
        print("B01 --%s-- vs --%s--" % (neighbor1, neighbor2))
        '''
        
        if indxEnd != -1:  # found
          indxEnd = indxEnd+1
          strTgt  = strTemp[indxStart:indxEnd]
          #strTgt  = strTemp[indxStart:indxStart*2]
          strTgt1 = strTgt[1:]
          #print("333:: @@@ @@@strTgt[%s], strTgt1[%s]" % (strTgt, strTgt1))
          if strTgt1.find(tagStart) != -1:   # found <…<…> do nothing
            print("<…<…> Error::%s" % (strTgt))
            lpCondition = False
          else:
            ###print("REM:: remove:%s" % (strTemp[indxStart:indxEnd]))
            strFront = strTemp[:indxStart]
            strBack  = strTemp[indxEnd:]
            strTemp  = strFront + strBack
            ###print("RES:: %s" % (strTemp))
            ###print("------------------\n")
          cntLoop += 1
          #input("Enter any key to proceed")
        else:  # tagEnd isnot found -> "<…"
          print(";;;")
          lpCondition = False
      else:
        lpCondition = False
      
    return strTemp

    
  def getUrlBase(self):
    '''
    return
    http://www.xyz.com/def/
    of
    http://www.xyz.com/def/abc.html
    '''
    lstExts = [".html", ".htm", ".php"]
    url = self.getUrl()
    for ext in lstExts:
      indxTgt = url.find(ext)
      if indxTgt != -1:   # found
        indxSLA = url.rfind("/")
        strTemp = url[:indxSLA+1]
        return strTemp
    return url
    
    
    

  def printInfo(self, printLink = False):
    ###print(self._soup.prettify())
    result = self._soup.find_all('p') 
    
    print("printing...")
    print("#lenResult: ", len(result))
    if printLink == True:
      for elem in result: 
         print(elem)###.encode("utf-8")) this causes hex string to be pronted!!!

        # for i in final_list: 
        #   print (i)
        # print (final_list)
    else:
      print(self._soup.prettify())

  def cleanseAll(self, strSrc):
    strSrc = self._reHtmlCode.sub("", strSrc)
    strSrc = self._rePunct.sub("", strSrc)
    strSrc = self._reFormat.sub("", strSrc)
    return strSrc
    
  def cleanseHtmlCode(self, strSrc):
    strSrc = self._reHtmlCode.sub("", strSrc)
    return strSrc

  def cleansePunct(self, strSrc):
    strSrc = self._rePunct.sub("", strSrc)
    return strSrc

  def cleanseFormat(self, strSrc):
    strSrc = self._reFormat.sub("", strSrc)
    return strSrc

  

  def html2Str(self, strHtml):
    self._dctHtml2Str = {
    	"." : "DOT",
    	"/" : "SLA",
    	":" : "SEM",
    	"," : "COM"
    	}
    	
    '''
    Convert typical HTML address to str
    www.abc-def.com/index.html
    to
    wwwDOTabc-defDOTcomSLAindexDOThtml
    '''
    strTarget = strHtml
    keys = self._dctHtml2Str.keys()
    for key in keys:
      val = self._dctHtml2Str.get(key)
      strTarget = strTarget.replace(key, val)
    print("---"*8)
    print("strTarget::%s " % (strTarget))
    return strTarget
    

  def str2Html(self, strSrc):
    '''
    Revert typical HTML converted str to address
    wwwDOTabc-defDOTcomSLAindexDOThtml
    to
    www.abc-def.com/index.html
    
    '''
    strTarget = strSrc
    vals = self._dctHtml2Str.values()
    keys = self._dctHtml2Str.keys()
    for val in vals:
      for key in keys:
        valk = self._dctHtml2Str.get(key)
        if val == valk:
          strTarget = strTarget.replace(val, key)
    
    print("---"*8)
    print("strTarget::%s " % (strTarget))
    return strTarget
    
class UrlNewsBase ():
  def __init__(self, url):
    self._headers = {#'Accept':'text/css,*/*;q=0.1', 
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.3', 
    'Accept-Encoding':'gzip,deflate,sdch', 
    'Accept-Language':'en-US,en;q=0.8', 
    #'User-Agent':'Mozilla/5 (Solaris 10) Gecko'} 
    'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'}
    
    self.lstSoupAllParagraphs = None
    self.lstSoupAllLinks = None
    self._request  = None
    self._response = None
    self._url = url
    
    # html codes
    self._ptnHtmlCode = '&#[0-9]+[;]'
    self._reHtmlCode  = re.compile(self._ptnHtmlCode)
    self._ptnPunct    = '[><}{)(.,"]+'
    self._rePunct     = re.compile(self._ptnPunct)
    self._ptnFormat   = '&[a-zA-Z;]+'
    self._reFormat    = re.compile(self._ptnFormat)

  def makeSoup (self):
    print ("------- makeSoup -------")
    self._soup = BeautifulSoup(self._response, "html.parser")
    self.lstSoupAllParagraphs = self._soup.find_all("p")
    self.lstSoupAllLinks = self._soup.find_all("a")
    ###print ( self._soup.prettify ())
    print ("<<<<<<< makeSoup >>>>>>>")
    
  
  def getSiteResponse (self):
    print ("-------> getSiteResponse -------")
    self._request  = request.Request(self._url, None, self._headers)
    self._response = request.urlopen( self._request )
    self._response = self._response.read ()
    print (">>>>>>>\n", self._response)
    print ("------- getSiteResponse <-------")
    
    '''
    # These are for compressed sites only.
    data = gzip.decompress(response.read()) 
    data = str(data,'utf-8')
    '''
    
  def _collectStats (self, lstTarget):
    cnt = 0
    for item in lstTarget:
      cnt += 1
    return cnt
    
  def printStats (self):
    print ("------- printStats -------")
    print ("num paragraphs ::%d" % (self._collectStats  (self.lstSoupAllParagraphs)))
    print ("num aLinks ::%d" % ( self._collectStats ( self.lstSoupAllLinks)))

  def printInfo(self, printLink = False):
    ###print(self._soup.prettify())
    result = self._soup.find_all('p') 
    
    print("printing...")
    print("#lenResult: ", len(result))
    if printLink == True:
      for elem in result: 
         print(elem)###.encode("utf-8")) this causes hex string to be pronted!!!

        # for i in final_list: 
        #   print (i)
        # print (final_list)
    else:
      print(self._soup.prettify())

  def cleanseAll(self, strSrc):
    strSrc = self._reHtmlCode.sub("", strSrc)
    strSrc = self._rePunct.sub("", strSrc)
    strSrc = self._reFormat.sub("", strSrc)
    return strSrc
    
  def cleanseHtmlCode(self, strSrc):
    strSrc = self._reHtmlCode.sub("", strSrc)
    return strSrc

  def cleansePunct(self, strSrc):
    strSrc = self._rePunct.sub("", strSrc)
    return strSrc

  def cleanseFormat(self, strSrc):
    strSrc = self._reFormat.sub("", strSrc)
    return strSrc

  def html2Str(self, strHtml):
    self._dctHtml2Str = {
    	"." : "DOT",
    	"/" : "SLA",
    	":" : "SEM",
    	"," : "COM"
    	}
    	
    '''
    Convert typical HTML address to str
    www.abc-def.com/index.html
    to
    wwwDOTabc-defDOTcomSLAindexDOThtml
    '''
    strTarget = strHtml
    keys = self._dctHtml2Str.keys()
    for key in keys:
      val = self._dctHtml2Str.get(key)
      strTarget = strTarget.replace(key, val)
    print("---"*8)
    print("strTarget::%s " % (strTarget))
    return strTarget
    
  def str2Html(self, strSrc):
    '''
    Revert typical HTML converted str to address
    wwwDOTabc-defDOTcomSLAindexDOThtml
    to
    www.abc-def.com/index.html
    
    '''
    strTarget = strSrc
    vals = self._dctHtml2Str.values()
    keys = self._dctHtml2Str.keys()
    for val in vals:
      for key in keys:
        valk = self._dctHtml2Str.get(key)
        if val == valk:
          strTarget = strTarget.replace(val, key)
    
    print("---"*8)
    print("strTarget::%s " % (strTarget))
    return strTarget
    
  def getAllParagraphText(self, output2File = False):
    if output2File:
      #fBase = "/storage/0123-4567/church/endtime/"
      fBase = "/storage/emulated/0/Documents/"
      fn = fBase + self.html2Str(self._url) + ".txt"
      fd = open(fn, "w")
    
    indxCnt = 1
    print("len::%d" % (len(self.lstSoupAllParagraphs)))
    for paragraph in self.lstSoupAllParagraphs:
      sep = "=="*8
      #strResult = self.cleansePunct(paragraph.text)
      strResult = self.cleanseFormat(paragraph.text)
      entry = "%d::%s" % (indxCnt, strResult)
      if strResult.isspace() == False:
        print(sep)
        print(entry)
        indxCnt += 1
        if output2File:
          fd.write(sep+"\n")
          fd.write(entry+"\n")
    numEntries = ("self._url:: %s" % (self._url))
    print(numEntries)
    if output2File:
      fd.write(sep+"\n")
      fd.close()
      
  def criticalKeywordSearch (self, strTarget):
    for keyw in self._criticalKeywords:
      if strTarget.find ( keyw ) != -1:  # found
        print ("%s found in news" % ( keyw ))
        print ("in website: %s" % (self._url))
        input ("Hit enter to continue!")
        
  def getAllLinks(self, output2File = False, optLnkText = False):
    print("-------getAllLinks-------")
    cnt = 1
    print ("type: self.lstSoupAllLinks:", type (self.lstSoupAllLinks))
    #print ("self.lstSoupAllLinks[0]:", self.lstSoupAllLinks[0])
    
    for lnk in self.lstSoupAllLinks:
      print("###"*9)
      if optLnkText == False:
        print("lText[%d]::\n%s"%(cnt, lnk))
      else:   # True get text part of <a>
        lText = lnk.get_text(strip=True)
        lText = str(lText)
        if lText.isspace() == False:
          ###if lText != "":
          ###if lText.isspace() == False:
            print("lText[%d]::\n>>%s<<" % (cnt, lText))
            self.criticalKeywordSearch(lText)
        else:
          print("lText[%d]:: empty" % (cnt))

      cnt += 1
    if self.lstSoupAllLinks == None:
      print (" self.lstSoupAllLinks is None")
    else:
      print("numLnks::%d"%(len(self.lstSoupAllLinks)))


  def removeTags(self, strTgt, strTag, strRep):
    strTemp = strTgt
    strTemp = strTemp.replace(strTag, strRep)
    
    return strTemp

  def removeLinks(self, strSrc):
    ptnTa   = "<a"
    ptnTail = ">"
    ptnT_a  = "</a>"
    strTgt = strSrc
    
    cntTa = strTgt.count(ptnTa)
    #obj = self._dctReplaceTags
    
    for i in range( cntTa ):
      indxPtnTa   = strTgt.find(ptnTa)
      strFront    = strTgt[: indxPtnTa]
      strTemp     = strTgt[ indxPtnTa :]
      indxPtnTail = strTemp.find( ptnTail )
      indxPtnTail = indxPtnTa + indxPtnTail
      strBack     = strTgt[ indxPtnTail+1 :]
      strRem      = strTgt[ indxPtnTa: indxPtnTail+1]
      
      print("indexes@@%d::%d  " % ( indxPtnTa, indxPtnTail ))
      print("Str = %s" % ( strRem ))
      
      strTgt = strFront + strBack
      
      # replace tags
      keys = self._dctReplaceTags.keys()
      for key in keys:
        strTag = key
        strRep = self._dctReplaceTags[key]
        strTgt = self.removeTags(strTgt, strTag, strRep)
      
    return strTgt
    
    
  def printSoupBodyByItem(self, fd = ""):
    body = self.getSoup().body
    indxBdy = 1
    if fd != "":
      for item in body:
        fd.write("÷÷÷"*12)
        strItem = "\n@@@%d == %s" % (indxBdy, item)
        strItem = self.removeLinks( strItem )
        fd.write(strItem)
        indxBdy += 1
      fd.close()
    else:     
      for item in body:
        print("÷÷÷"*12)
        print("\n@@@%d == %s" % (indxBdy, item))
        indxBdy += 1
      
    print("numBdyItems = %d" % (indxBdy))
    
  def scraperCollect(self):
    keys = self._bblBooks.keys()
    for key in keys:
      url   = key
      fname = "/storage/emulated/0/Documents/" + self._bblBooks[key] + ".txt"
      fd = open(fname,"w")
      # regeneration of soup tree
      print('### url, "big5", True ###')
      self.myinit(url, "big5", True)
      #self.myinit(url)
      self.printSoupBodyByItem(fd)
      print("...,,,"*7)
      print("\n")
