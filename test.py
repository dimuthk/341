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
  def __init__(self, anchors):
    xml.sax.ContentHandler.__init__(self)
    self.title = ""
    self.ignore = False
    self.get_text = False
    self.get_title = True
    self.in_page = False
    self.text = ""
    self.cnt = 0
    self.anchors = anchors
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


  def endElement(self, name):
    if name == 'page' and self.ignore == False:
        self.in_page = False
        self.cnt += 1
        if self.cnt % 1000 == 0:
          print(self.cnt)

        #DEBUG
        mid = lambda x: re.sub(r'([^\s\w]|_)+', ' ', x.lower().replace('\n',''))
        anum2 = lambda x: ' '.join([word for word in mid(x).split()])
        matches = re.findall('\[\[.*?\]\]', self.text)
        matches = [match[2:-2] for match in matches]
        for i in range(len(matches)):
          if '|' in matches[i]:
            matches[i] = matches[i].split('|')[1]
          matches[i] = matches[i].split('#')[0]

        for i in range(len(matches)):
          if self.isStop(matches[i]):
            matches[i] = ''
        
        orig = self.text

        matches = [anum2(match) for match in matches]

        anum = lambda x: re.sub(r'([^\s\w]|_)+', ' ', x.lower().replace('\n',''))
        self.text = anum(self.text) #return only alpha numeric + spaces
        self.text = ' '.join([word for word in self.text.split()])

        
        words = self.text.split()
        words = [word.strip() for word in words]
 
        

        total = list()
        grams_arr = [zip(words), zip(words, words[1:]), zip(words, words[1:], words[2:]), \
                 zip(words,words[1:],words[2:],words[3:]), \
                 zip(words,words[1:],words[2:],words[3:],words[4:])]
        
        for grams in grams_arr:
          for gram in grams:
              gram_str = reduce(lambda x,y: x+' '+y,gram)
              total.append(gram_str)

              if gram_str in self.anchors:
                self.anchors[gram_str] += 1

        for match in matches:
          if match not in total and len(match.split(' ')) < 6 and match != '':
            pdb.set_trace()
        
        
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


for fnum in range(int(sys.argv[1]), int(sys.argv[2])):
  handler = AnchorTextCntContentHandler(anchors)
  xml.sax.parse(open("../../cs341/wiki_sub/" + str(fnum) + '.xml'), handler)
  print('tallied anchor counts for ' + str(fnum))

  with open('../anchors_tally/' + str(fnum),'w') as f:
    if debug == False:
      for key in handler.anchors.keys():
        f.write(key + '<>' + str(handler.anchors[key]) + '\n')
  print('wrote anchor counts for ' + str(fnum))

  for key in anchors.keys():
    anchors[key] = 0
  

