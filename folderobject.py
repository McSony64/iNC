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
import os

class folderObject(object):
  def __init__(self, fPath):
    self._folderPath = fPath

  def renameFileSet(self, ptnOld, ptnNew):
    cntRename = 0
    for filename in os.listdir(self._folderPath):
      print("fn = %s" % (filename))
      if filename.startswith(ptnOld):
        newFN = filename
        newFN = newFN.replace(ptnOld, ptnNew)
        newFN = self._folderPath + newFN
        oldFN = self._folderPath + filename
        print("oldFN = %s, newFN = %s" % (oldFN, newFN))
        os.rename(oldFN, newFN)
        cntRename += 1
    print("%d files renamed in \n%s" % (cntRename, self._folderPath))
    
  def moveFileSet(self, fDesPath):
    pass
    
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
    print("processTrimFile(fname[%s])" % (fname))
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
      
      print("\n\nFile changes:")
      print("-------"*5)
      print("original line cnt = %d" % (cntLines01))
      print("removed leading %d lines" % (cntLeadingMax))
      print("remved trailing %d lines" % (cntTrailing))
      print("modified line cnt = %d" % (cntLines02))
      print("======="*5+"\n\n")
    return lstLines
      
          
  def trimFiles(self, iStart, iEnd, fBase, fExt, fZfill):
    for i in range(iStart, iEnd):
      if fZfill > 0:
        ff = fBase + str(i).zfill(fZfill) + fExt
      else:
        ff = fBase + str(i) + fExt
      #fg = fBase + "xyz" + str(i) + fExt
      print("trimFiles:: ff[%s]" % (ff))

      '''
      lstRes  = self.processTrimFile(ff)
      
      fn = open(ff, "w")
      for line in lstRes:
        fn.write(line)
      fn.close()

      fn = open(ff)
      print(">>> %d lines written in " % (len(fn.readlines())))
      print(">>>>>>> %s <<<<<<<\n\n" % (str(i) + fExt))
      fn.close()
      '''
      self.trim1File(ff)


  def trim1File(self, fname):
    lstRes = self.processTrimFile(fname)
    fn = open(fname, "w")
    for line in lstRes:
      fn.write(line)
    fn.close()

    fn = open(fname)
    print(">>> %d lines written in " % (len(fn.readlines())))
    print(">>>>>>> %s <<<<<<<\n\n" % (fname))
    fn.close()



def main():
  fPath = "/storage/emulated/0/documents/"
  fObject = folderObject(fPath)

  ''' done  
  ptnOld = "xbls"
  ptnNew = "希伯來書"
  fObject.renameFileSet(ptnOld, ptnNew)
  
  fPrefix = "ccgn_護教手冊_"
  fBase   = fPath + fPrefix
  fExt    = ".txt"
  '''
  ''' done
  iStart  = 1
  iEnd    = 16   # indicating 1 to 15  
  fZfill  = 2
  fObject.trimFiles(iStart, iEnd, fBase, fExt, fZfill)
  
  fname = fBase + "index" + fExt
  fObject.trim1File(fname)
  '''

  ptnOld = "ccgn_聖經如此說"
  ptnNew = "ccgn_家是愛之窩"
  fObject.renameFileSet(ptnOld, ptnNew)



if __name__ == "__main__":
  main()
