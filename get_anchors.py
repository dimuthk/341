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
  def __init__(self, raw, redirects):
    xml.sax.ContentHandler.__init__(self)
    self.title = ""
    self.get_text = False
    self.get_title = True
    self.in_page = False
    self.debug = False
    self.raw = raw #raw anchor<>entity dump
    self.text = ""
    self.cnt = 0
    self.stops = ['Media','Special','Talk','User','User talk', 'Wikipedia',\
         'Wikipedia talk', 'File', 'File talk', 'MediaWiki',\
         'MediaWiki talk','Template','Template talk','Help',\
         'Help talk','Category','Category talk','Portal',\
         'Portal talk','Book','Book talk','Education Program',\
         'Education Program talk','TimedText','TimedText talk',\
         'Module','Module talk']
    self.redirects = redirects
    
    mid = lambda x: re.sub(r'([^\s\w]|_)+', ' ', x.lower().replace('\n',''))
    self.anum = lambda x: ' '.join([word for word in mid(x).split()])
    
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

  def isStop(self,word):
    for stop in self.stops:
      if stop + ':' in word:
        return True
    return False

 
  def endElement(self, name):
    if name == 'page' and self.ignore == False:
        self.in_page = False
        self.cnt += 1
        if self.cnt % 1000 == 0:
          print(self.cnt)
          
        #retrieve and print anchor texts/entities.
        matches = re.findall('\[\[.*?\]\]', self.text)

        self.title = self.title.split('#')[0]
        
        for match in matches:
            match = match[2:-2] #trim '[[' and ']]'
            if '|' in match:
                parts = match.split('|')
                entity = parts[0].split('#')[0].strip()
                anchor = parts[1].split('#')[0].strip()

            else:
                entity = match.split('#')[0].strip()
                anchor = match.split('#')[0].strip()

            
            if self.isStop(self.title) or self.isStop(entity) or self.isStop(anchor):
              continue

            title = self.anum(self.title)
            entity = self.anum(entity)
            anchor = self.anum(anchor)

            if title in self.redirects:
              title = self.redirects[title]
            if entity in self.redirects:
              entity = self.redirects[entity]
            #if anchor in self.redirects:
             # anchor = self.redirects[anchor]


            self.raw.write(title + '<>' + entity + '<>' + anchor + '\n')
                
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

redirects = {}
for line in open('../redirects','r'):
  parts = line.split('<>')
  title = parts[0].strip()
  if len(title.split()) > 5:
    continue
  redir = parts[1].strip()
  redirects[title] = redir

if '' in redirects:
  del redirects['']
  
print 'got redirects'

for fnum in range(int(sys.argv[1]), int(sys.argv[2])):
  print('starting ' + str(fnum))
  raw = open('../anchors_anum/' + str(fnum),'w')
 
  xml.sax.parse(open("../wiki_sub/" + str(fnum) + '.xml'), WikiContentHandler(raw, redirects))

  raw.close()
  print('finished ' + str(fnum))

