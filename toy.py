import xml.sax
import re
import pdb
import sys
import os

#THIS CODE IS MADE FOR PYTHON 3.0+
#use a SAX parser to retrieve the following info from the wiki set:
#page_title<>link_destination<>anchor_text

#CMD INPUT
#wiki_sub/start_num, end_num

#OUTPUT
#anchors_raw/n



class WikiContentHandler(xml.sax.ContentHandler):
  def __init__(self):
    xml.sax.ContentHandler.__init__(self)
    self.title = ""
    self.get_text = False
    self.get_title = True
    self.in_page = False
    self.raw = open('../toy/' + str(0),'w')
    self.text = ""
    self.cnt = 0
    self.found = 0
    
  def startElement(self, name, attrs):
    if name == 'page': #new page
        self.in_page = True
        self.ignore = False
        self.title = ""
        self.text = ""


    elif name == 'title':
        self.get_title = True

    elif name == 'text':
        self.get_text = True
 
  def endElement(self, name):
    if name == 'page' and self.ignore == False:
        self.in_page = False

        if len(self.text) > 1000:
          self.found += 1
          self.raw.write(self.title + '\n' + self.text)
          self.raw.close()
          self.cnt += 1
          self.raw = open('../toy/' + str(self.cnt),'w')
          
          

    if self.found == 100:
        self.raw.close()
        sys.exit('Done')
                
    elif name == 'title' and self.in_page == True:
        self.get_title = False

    elif name == 'text':
        self.get_text = False       
                    
         
  def characters(self, content):
    if self.in_page == True:
        if self.get_text == True:
            self.text += content
            
        elif self.get_title == True:
            self.title += content


if len(sys.argv) != 3:
  sys.exit('usage: python get_anchor_cnts.py start_num end_num')



for fnum in range(int(sys.argv[1]), int(sys.argv[2])):
  print('starting ' + str(fnum))
 
  xml.sax.parse(open("../wiki_sub/" + str(fnum) + '.xml'), WikiContentHandler())

  print('finished ' + str(fnum))

