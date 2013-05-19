import xml.sax
import re
import os
import pdb
import sys

#THIS CODE IS MADE FOR PYTHON 3.0+
#use a SAX parser to retrieve frequency counts for the anchor_texts
#listed in anchors_anum, the alphanumeric anchor-text list.

#upload set of unique anchor texts to memory, run SAX parser through
#wiki dataset. for each text block, retrieve alphanumeric + space characters,
#tokenize words. retrieve 1-5 n-grams using zip. generate frequency counts
#accordingly by checking hashes to document.

#print resultant hash table to file.

#NEEDS
#anchors_anum/0, 1, ..., n

#CMD INPUT
#wiki_sub/start_num.xml, end_num.xml

#OUTPUT
#anchors_tally/start_num, (start_num+1), ..., end_num

 
class AnchorTextCntContentHandler(xml.sax.ContentHandler):
  def __init__(self, anchors, redirects):
    xml.sax.ContentHandler.__init__(self)
    self.title = ""
    self.ignore = False
    self.get_text = False
    self.get_title = True
    self.in_page = False
    self.text = ""
    self.cnt = 0
    self.anchors = anchors
    self.redirects = redirects
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

  def isStop(self, word):
    for stop in self.stops:
      if word in stop + ':':
        return True
    return False

  def ascii(self,char):
    asc = ord(char)
    if asc > 47 and asc < 58: #number
      return True
    if asc > 64 and asc < 91: #capital
      return True
    if asc > 96 and asc < 122: #lowercase
      return True
    return False


  def toAscii(self, text):
    for i in range(len(text)):
      if not self.ascii(text[i]):
        text[i] = ' '
    return text


  def endElement(self, name):
    if name == 'page' and self.ignore == False:
        self.in_page = False
        self.cnt += 1
        if self.cnt % 1000 == 0:
          print(self.cnt)

#        matches = re.findall('\[\[.*?\]\]', self.text)

#        for match in matches: #consider the anchor texts separately
#          self.text = self.text.replace(match,'<>')

        mid = lambda x: re.sub(r'([^\s\w]|_)+', ' ', x.lower().replace('\n',''))
        anum = lambda x: ' '.join([word for word in mid(x).split()])


        self.text = anum(self.text) #return only alpha numeric + spaces
  

        words = self.text.split()
        words = [word.strip() for word in words]

        

        grams_arr = [zip(words), zip(words, words[1:]), zip(words, words[1:], words[2:]), \
                 zip(words,words[1:],words[2:],words[3:]), \
                 zip(words,words[1:],words[2:],words[3:],words[4:])]
        for grams in grams_arr:
          for gram in grams:
              gram_str = reduce(lambda x,y: x+' '+y,gram)
#              if gram_str in self.redirects:
#                gram_str = self.redirects[gram_str]

              
              if gram_str in self.anchors:
                self.anchors[gram_str] += 1

                
    elif name == 'title' and self.in_page == True:
        self.get_title = False

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


debug = False
anchors = {}
#read in anchor_texts_anum page
for fname in os.listdir('../anchors_anum/'):
  for line in open('../anchors_anum/' + fname,'r'):
    anchors[line.split('<>')[2].strip()] = 0

print('initialized hash map. num words: ' + str(len(anchors.keys())))

redirects = {}
a = '''
for line in open('../redirects','r'):
  parts = line.split('<>')
  title = parts[0].strip()
  if len(title.split()) > 5:
    continue
  redir = parts[1].strip()
  redirects[title] = redir

if '' in redirects:
  del redirects['']
'''  
print 'got redirects'



for fnum in range(int(sys.argv[1]), int(sys.argv[2])):
  handler = AnchorTextCntContentHandler(anchors,redirects)
  xml.sax.parse(open("../wiki_sub/" + str(fnum) + '.xml'), handler)
  print('tallied anchor counts for ' + str(fnum))

  with open('../anchors_tally/' + str(fnum),'w') as f:
    if debug == False:
      for key in handler.anchors.keys():
        f.write(key + '<>' + str(handler.anchors[key]) + '\n')
  print('wrote anchor counts for ' + str(fnum))

  for key in anchors.keys():
    anchors[key] = 0
  

