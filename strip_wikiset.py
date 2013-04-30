import xml.sax
import re
import sys 
import pdb
import cgi

#THIS CODE IS MADE FOR PYTHON 3.0+
#split the wiki dataset into multiple parts.
#each part should only contain
#<page>
#<title>TITLE</title>
#<text>TEXT</text>
#</page>
#exclude all pages that are revisions, all pages with titles containing File: Special:, etc.
#each wiki subdataset should contain 500,000 pages.

#NEEDS
#enwiki-latest-pages-articles.xml

#OUTPUT
#wiki_sub/0.xml, 1.xml, ... n.xml



 
class AnchorTextCntContentHandler(xml.sax.ContentHandler):
  def __init__(self,f):
    xml.sax.ContentHandler.__init__(self)
    self.title = ""
    self.ignore = False
    self.get_text = False
    self.get_title = True
    self.in_page = False
    self.f = f
    self.text = ""
    self.cnt = 0
    self.fail = 0
    self.chars = 100000000
    self.curr_num = 0
    self.cnter = 0
    self.curr_file = open("wiki_sub/" + str(self.curr_num) + ".xml", "w")
    self.curr_file.write('<root>\n')
    self.uniq = set()
    self.stops = ['Media','Special','Talk','User','User talk', 'Wikipedia',\
                  'Wikipedia talk', 'File', 'File talk', 'MediaWiki',\
                  'MediaWiki talk','Template','Template talk','Help',\
                  'Help talk','Category','Category talk','Portal',\
                  'Portal talk','Book','Book talk','Education Program',\
                  'Education Program talk','TimedText','TimedText talk',\
                  'Module','Module talk']
   
  def startElement(self, name, attrs):
    if name == 'page': #new page
        self.in_page = True
        self.ignore = False
        self.title = ""
        self.text = ""

    elif name == 'redirect': #a redirect:
        self.ignore = True

    elif name == 'title':
        self.get_title = True

    elif name == 'text':
        self.get_text = True

  def goodText(self, name):
    for stop in self.stops:
      if (stop + ':') in name:
        return False
    return True
 
  def endElement(self, name):
    if name == 'page' and self.ignore == False:
        self.in_page = False
        self.cnt += 1
        if self.cnt % 1000 == 0:
          print(self.cnt)
        if self.cnt % 35000 == 0:
          self.curr_file.flush()
          self.curr_file.write('</root>')
          self.curr_file.close()
          self.curr_num += 1
          self.curr_file = open("wiki_sub/" + str(self.curr_num) + ".xml", "w")
          self.curr_file.write('<root>\n')

        self.curr_file.write("<page>\n")
        self.curr_file.write("<title> " + cgi.escape(self.title) + "</title>\n")
        self.curr_file.write("<text>\n")
        
        if len(self.text) > 0 and self.text[-1] == '\n':
          self.text = self.text[:-1]

        self.curr_file.write(cgi.escape(self.text) + "\n")        
        self.curr_file.write("</text>\n")
        self.curr_file.write("</page>\n")

                
    elif name == 'title' and self.in_page == True:
        self.get_title = False
        #trim '#' signs, and ignore this page if title is of below form.
        if self.goodText(self.title) == False:
            self.ignore = True
        else:
            self.title = self.title.split('#')[0].strip()


    elif name == 'text':
        self.get_text = False       
                    
         
  def characters(self, content):
    self.cnter += 1
    if self.cnter >= 100000:
      self.cnter = 0
      if self.f.tell() > self.chars:
        print('Chars read: ' + str(self.chars/1000000) + ' M')
        self.chars += 100000000
    
    if self.ignore == False and self.in_page == True:
        if self.get_text == True:
            self.text += content
            
        elif self.get_title == True:
            self.title += content


f = open("enwiki-latest-pages-articles.xml")
handler = AnchorTextCntContentHandler(f)
xml.sax.parse(f, handler)
handler.curr_file.write('</root>')
handler.curr_file.close()
f.close()

