import xml.sax
import re
import sys 
import pdb
import cgi

#FORMAT:
#text<>redirect

#NEEDS
#wiki_sub/0.xml, 1.xml, ... n.xml

#OUTPUT
#redirects


 
class AnchorTextCntContentHandler(xml.sax.ContentHandler):
  def __init__(self,f):
    xml.sax.ContentHandler.__init__(self)
    self.title = ""
    self.ignore = True
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
    self.curr_file = open("../redirects", "w")
    
   
  def startElement(self, name, attrs):
    if name == 'page': #new page
        self.cnt += 1
        if self.cnt % 100000 == 0:
          print self.cnt
        self.in_page = True
        self.ignore = True
        self.title = ""
        self.text = ""

    elif name == 'redirect': #a redirect:
        self.ignore = False

    elif name == 'title':
        self.get_title = True

    elif name == 'text':
        self.get_text = True

  def endElement(self, name):
    if name == 'page' and self.ignore == False:
        self.in_page = False
        self.cnt += 1
        matches = re.findall('\[\[.*?\]\]', self.text)
        
        mid = lambda x: re.sub(r'([^\s\w]|_)+', ' ', x.lower().replace('\n',''))
        anum = lambda x: ' '.join([word for word in mid(x).split()])
        self.title = self.title.split('#')[0]

        redir = matches[0][2:-2].split('#')[0]
        self.curr_file.write(anum(self.title) + '<>' + anum(redir) + '\n')

                
    elif name == 'title' and self.in_page == True:
        self.get_title = False

    elif name == 'text':
        self.get_text = False       
                    
         
  def characters(self, content):
    if self.get_text == True and self.ignore == False:
      self.text += content
            
    elif self.get_title == True:
      self.title += content


f = open("../../cs341/enwiki-latest-pages-articles.xml")
handler = AnchorTextCntContentHandler(f)
xml.sax.parse(f, handler)
handler.curr_file.close()
f.close()

