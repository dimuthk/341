## For trial on Dimuth's computer.

import operator
import copy
import re
import itertools
import pdb
import marshal
import time

start = 1
stop = 11

beg = time.time



#read dictionaries from file
anchors = marshal.load(open('anchors.obj','rb'))
entities = marshal.load(open('entities.obj','rb'))
#entity_id = marshal.load(open('entity_id.obj','rb'))

print 'uploaded dictionaries'

#numbers, already sorted
def similarity(list1, list2):
  (inter,uni) = (0,0)
  (i,j) = (0,0)
  while i < len(list1) and j < len(list2):
    if list1[i] < list2[j]:
      i += 1
    elif list2[j] < list1[i]:
      j += 1
    else:
      inter += 1
      (i,j) = (i+1,j+1)
    uni += 1
  
  uni += (len(list1) - i) + (len(list2) - j)
  return float(inter) / uni



#get_alphanumeric text from a given file
get_clean_text = lambda fname: reduce(lambda x,y: x+y, open(fname,'r').readlines()).replace('\n','')
anum = lambda x: re.sub(r'([^\s\w]|_)+', '', get_clean_text(x).lower())

#retrieve proper space-delimited ngrams from a text block
get_raw_grams = lambda words: [zip(words),zip(words,words[1:]),zip(words,words[1:],words[2:]),\
  zip(words,words[1:],words[2:],words[3:]), zip(words,words[1:],words[2:],words[3:],words[4:])]
get_ngrams = lambda text: [map(lambda tup:reduce(lambda x,y: x+' '+y,tup),grams) for grams in get_raw_grams(text.split())]

for doc in range (start, stop):
    print 'Processing Doc: ', doc
    input_file = 'article' + str(doc) + '.txt'

    #get alpha-numeric text from the file
    anum_text = anum(input_file) #return only alpha numeric + spaces

    #get n-grams
    grams_arr = get_ngrams(anum_text)
    
    print 'got ngrams'

    #anchors_in_doc = {}
    #anchors_in_doc_lp = {}

    anchors_in_doc = list()

    for grams in grams_arr:
      for gram in grams:
        if gram in anchors:
          anchors_in_doc.append(gram)
               # if new_gram not in anchors_in_doc:
                #    anchors_in_doc[new_gram] = copy.deepcopy(anchors[new_gram])
                 #   anchors_in_doc_lp[new_gram] = copy.deepcopy(anchors_lp[new_gram])
    
    
    print 'got anchors in doc'
    print len(anchors_in_doc)

    #entities_in_doc = {}
    #entities_in_doc = list()

   # for anch in anchors_in_doc:
        
    #    for ent_ref in anchors[anch]:
     #       if ent_ref in entities_:
      #          ent = entity_id[ent_ref]
       #         entities_in_doc[ent] = entities(ent_ref)
      #for ent in anchors[anch]:
       # if ent in entities_:
        #  entities_in_doc.append(ent)

    #unambig = {}
    #ambig = {}
    print 'got entities in doc'

    unambig = list()
    ambig = list()

    for key1 in anchors_in_doc:
      if len(anchors[key1][1]) == 1:
        unambig.append(key1)
      else:
        ambig.append(key1)
    #        if key1 not in unambig:
    #            unambig[key1] = copy.deepcopy(anchors_in_doc[key1])
    #    else:
    #        if key1 not in ambig:
    #            ambig[key1] = copy.deepcopy(anchors_in_doc[key1])


    

    print len(ambig)
    print len(unambig)

    avg_sim = {}
    cnt = 0
    for key1 in unambig:
        cnt += 1
        if cnt % 10 == 0:
          print len(anchors[key1][1])
        for ent1_ref in anchors[key1][1]:
            avg_sim[ent1_ref] = 0
            for key2 in unambig:
                for ent2_ref in anchors[key2][1]:
                    if ent1_ref != ent2_ref:
                        if (ent1_ref in entities) & (ent2_ref in entities):
                            inter = len(set(entities[ent1_ref]).intersection(set(entities[ent2_ref])))
                            uni = len(set(entities[ent2_ref]).union(set(entities[ent2_ref])))
                            #inter = len((entities(ent1_ref)).intersection(entities(ent2)))
                            #uni = len((entities(ent1)).union(entities(ent2)))
                            sim = inter/(1.0*uni)
                            avg_sim[ent1_ref] += sim
        avg_sim[ent1_ref] = avg_sim[ent1_ref]/(1.0*(len(unambig)-1))

    print 'got avg sim'
    cnt = 0
    ambig_m = {}
    for key1 in ambig:
        cnt += 1
        if cnt % 10 == 0:
          print len(anchors[key1][1])
        for ent1_ref in anchors[key1][1]:
            ambig_m[(key1,ent1_ref)] = 0
            
            for key2 in unambig:
                for ent2_ref in anchors[key2][1]:
                    if (ent1_ref in entities) & (ent2_ref in entities):
                        #(ents1,ents2) = (entities(ent1),entities(ent2))
                        (ents1,ents2) = (entities[ent1_ref], entities[ent2_ref])
                        #inter = len((entities(ent1)).intersection(entities(ent2)))
                        #uni = len((entities(ent1)).union(entities(ent2)))
                        sim = similarity(ents1,ents2)
                        ambig_m[(key1,ent1_ref)] += anchors[key2][0]*avg_sim[ent2_ref]*sim

    f = open('output' + str(doc), 'w', 10000)

    print 'got ambig terms'

    disambiguated = {}
    for anch in ambig:
            if anchors[anch][0] > 0:
                    disambiguated[anch] = {}
                    for ent in anchors[anch][1]:
                            disambiguated[anch][ent] = anchors[anch][1][ent]*ambig_m[(anch,ent)]
                    max_disamb = max(disambiguated[anch].iteritems(), key=operator.itemgetter(1))
                    f.write(str(anch) + '\t' + str(anchors[anch][0]) + '\t' + str(max_disamb[0]) + '\t' + str(anchors[anch][1][max_disamb[0]]) + '\t' + str(ambig_m[(anch,max_disamb[0])])+ '\n')

    for anch in unambig:
        if anchors[anch][0] > 0.05:
            for ent in anchors[anch][1]:
                f.write(str(anch) + '\t' + str(anchors[anch][0]) + '\t' + str(ent) + '\t' + str(anchors[anch][1][ent]) + '\t' + str(0) + '\n')
    f.close()


print 'elapsed: ' + str(time.time - beg)
