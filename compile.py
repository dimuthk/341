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

def updateEntityList(entity, entity_list):
  trimmedList = [val[0] for val in entity_list]
  pos = [i for i,x in enumerate(trimmedList) if x == entity]
  if len(pos) > 0:

    entity_list[pos[0]] = (entity_list[pos[0]][0], entity_list[pos[0]][1] + 1)
  else:
    entity_list.append((entity,0))
  return entity_list

def stringify(entity_list):
  res = ""
  for item in entity_list:
    st = item[0] + '(' + str(item[1]) + ')'
    res += '<>' + st
  return res[2:]
 
#OUTPUt
#anchor_text<>numerator<>denominator<>entity1(cnt)<>entity2(cnt)
anchors = {}
for fname in os.listdir('anchors_anum/'):
  cnt = 0
  for line in open('anchors_anum/' + fname, 'r'):
    parts = line.split('<>')
    anchor = parts[2][:-1]
    entity = parts[1]
    
    if anchor in anchors:
      anchors[anchor].append(entity)
    else:
      anchors[anchor] = [entity]
    cnt += 1
    if cnt % 100000 == 0:
      print cnt

#pdb.set_trace()
print 'got entity cnts'
out = open('final','w')
for line in open('anchors_link_prob','r'):
  anchor = line.split('<>')[0]
  if anchor in anchors:
    entities = anchors[anchor]
    unique = set(entities)
    entities_str = ""
    for entity in unique:
      entities_str += '<>' + entity + '(' + entities.count(entity) + ')'
    out.write(line[:-1] + '<>' + entities_str[2:] + '\n')
out.close()
        
  

  

