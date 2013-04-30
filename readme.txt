Step 1
strip_wikiset.py:     enwiki-latest-pages-articles.xml -> wiki_sub/*
get_redirects.py:     enwiki-latest-pages-articles.xml -> redirects

Step 2
get_anchors.py:       wiki_sub/*, redirects -> anchors_anum/*

Step 3
get_anchor_cnts.py:   wiki_sub/*, redirects, anchors_anum/* -> anchors_tally/*

Step 4
get_link_prob.py:     anchors_anum/*, anchors_tally/* -> anchors_link_prob

Check
confirm.py:           anchors_link_prob -> num errors / total



