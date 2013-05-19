import marshal
import itertools
import pdb

anchors_file = 'comm_out'
entities_file = 'ent_out'

word_id = 0
anchors = {} #anchors[anchor] -> [1,5,6,8...]
entities = {} #entities[3] -> [1,5,7,9,...]
entity_id = {} #entitiy[3] -> [entity]
used_words = {} #entity[entity] -> 3

#add word references to entity_id
def add_word(word):
  global entity_id
  global word_id
  global used_words
  if word not in used_words:
    entity_id[word_id] = word
    used_words[word] = word_id
    word_id += 1

cnt = 0
print 'constructing anchors{}'
for line in open(anchors_file,'r',10000):
  line_text = line.strip().split('\t')
  
  anchor = line_text[0]
  if anchor not in anchors:
    anchors[anchor] = [0.5,{}] #lp, ent dict
    
    if int(line_text[2]) != 0:
      anchors[anchor][0] = float(line_text[1]) / int(line_text[2])

  for i in range(3, len(line_text), 2):
    add_word(line_text[i])
    ref = used_words[line_text[i]]
    if ref not in anchors[anchor][1]:
      anchors[anchor][1][ref] = float(line_text[i+1]) / int(line_text[1])



  cnt += 1
  if cnt % 100000 == 0:
    print cnt


marshal.dump(anchors, open('anchors.obj','wb'))
anchors.clear()

print 'constructing entities{}'
#this segment utilizes too much memory to allow for direct hashing. entities repeat several times! assign an id
#for each unique entity (build a map of this). then, build an entity map that points to these index values. this
#should be a substantial reduction in size. 
cnt = 0
f = open(entities_file,'r',10000)
get_tag = lambda line: ''.join(itertools.takewhile(lambda x: x!= '\t', line))
id_num = 0
for line in f:
  line_text = line.strip().split('\t')
  
  for word in line_text:
    add_word(word)

  ref = used_words[line_text[0]]
  entities[ref] = list()
  for entity in line_text[1:]:
    ref_sub = used_words[entity]
    entities[ref].append(ref_sub)

  entities[ref] = sorted(entities[ref])
  cnt += 1
  if cnt % 100000 == 0:
    print cnt

marshal.dump(entities, open('entities.obj','wb'))
entities.clear()

f.close()
print 'done'
