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
miss = 0
cnt = 0
for line in open('../anchors_link_prob','r'):
  parts = line.split('<>')
  text = parts[0]
  num = parts[1]
  den = parts[2]

  if len(text.split(' ')) < 6:
    if int(den) < int(num):
      print line[:-1]
      miss += 1
  cnt += 1


print str(miss) + '/' + str(cnt)
