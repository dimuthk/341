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
#anchors_anum/n



class WikiContentHandler(xml.sax.ContentHandler):
  def __init__(self, raw, anum):
    xml.sax.ContentHandler.__init__(self)
    self.title = ""
    self.ignore = False
    self.get_text = False
    self.get_title = True
    self.in_page = False
    self.raw = raw #raw anchor<>entity dump
    self.anum = anum #anchor texts only contain alphanumeric characters
    self.text = ""
    self.cnt = 0
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

  #the text does not contain a stop word as listed in __init__
  def goodTitle(self, name):
    for stop in self.stops:
      if name in stop:
        return False
    return True
 
  def endElement(self, name):
    if name == 'page' and self.ignore == False:
        self.in_page = False
        self.cnt += 1
        if self.cnt % 1000 == 0:
          print(self.cnt)
          
        #retrieve and print anchor texts/entities.
        matches = re.findall('\[\[.*?\]\]', self.text)
        mid = lambda x: re.sub(r'([^\s\w]|_)+', ' ', x.lower().replace('\n',''))
        anum = lambda x: ' '.join([word for word in mid(x).split()])
        
        for match in matches:
            match = match[2:-2] #trim '[[' and ']]'
            if '|' in match:
                parts = match.split('|')
                parts[0] = parts[0].split('#')[0].strip() #remove stuff after '#' sign
                parts[1] = parts[1].strip()
                parts[0] = ' '.join([word for word in parts[0].split()])
                parts[1] = ' '.join([word for word in parts[1].split()])
                if self.goodTitle(parts[0]) and self.goodTitle(parts[1]):
                  self.anum.write(anum(self.title) + "<>" + \
                                    anum(parts[0]) + "<>" + anum(parts[1]) + "\n")
                  self.raw.write(self.title + "<>" + parts[0] + "<>" + parts[1] + "\n")

            else: 
                match = match.split('#')[0].strip()
                match = ' '.join([word for word in match.split()])
                if self.goodTitle(match):
                  self.anum.write(anum(self.title) + "<>" + anum(match) + "<>" + \
                                    anum(match) + "\n")
                  self.raw.write(self.title + "<>" + match + "<>" + match + "\n")

      
                
    elif name == 'title' and self.in_page == True:
        self.get_title = False
        #trim '#' signs, and ignore this page if title is of below form.
        if self.goodTitle(self.title) == False:
            self.ignore = True
        else:
            self.title = self.title.split('#')[0].strip()

    elif name == 'text':
        self.get_text = False       
                    
         
  def characters(self, content):
    if self.ignore == False and self.in_page == True:
        if self.get_text == True:
            self.text += content
            
        elif self.get_title == True:
            self.title += content


if len(sys.argv) != 3:
  sys.exit('usage: python get_anchor_cnts.py start_num end_num')



for fnum in range(int(sys.argv[1]), int(sys.argv[2])):
  print('starting ' + str(fnum))
  raw = open('../anchors_raw/' + str(fnum),'w')
  anum = open('../anchors_anum/' + str(fnum),'w')
 
  xml.sax.parse(open("../wiki_sub/" + str(fnum) + '.xml'), WikiContentHandler(raw, anum))

  raw.close()
  anum.close()
  print('finished ' + str(fnum))

