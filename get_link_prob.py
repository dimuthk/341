import xml.sax
import re
import pdb
import sys
import os

#THIS CODE IS MADE FOR PYTHON 3.0+
#get link probabilities for anchor texts

#NEEDS
#anchors_anum
#anchors_tally

#OUTPUT
#anchors_link_prob

#FORMAT
#anchor_text<>num_links<>num_occurences

anchors = {}

for fname in os.listdir('../anchors_anum/'):
  for line in open('../anchors_anum/' + fname, 'r'):
    anc = line.split('<>')[2].strip()
    if anc in anchors:
      anchors[anc] = (anchors[anc][0] + 1, 0)
    else:
      anchors[anc] = (1,0)
  print(fname)

print 'got numerators'

for fname in os.listdir('../anchors_tally/'):
  for line in open('../anchors_tally/' + fname, 'r'):
    anc = line.split('<>')[0].strip()
    cnt = line.split('<>')[1].strip()
    anchors[anc] = (anchors[anc][0], anchors[anc][1] + int(cnt))
  print(fname)

print 'got denominators'

out = open('../anchors_link_prob','w')
for anc in sorted(anchors.keys()):
  out.write(anc + '<>' + str(anchors[anc][0]) + '<>' + str(anchors[anc][1]) + '\n')

out.close()  
  
