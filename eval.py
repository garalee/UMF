import QDToolGR
import SCToolGR


import numpy as np
from sklearn.feature_extraction import image
from sklearn.cluster import spectral_clustering


s = SCToolGR.SC()
g = QDToolGR.QDToolGR()


def inner_similarity(l):
    n = len(l)
    m = 0
    for i,p in enumerate(l):
        for j in range(i,n):
            if not i == j:
                m = max(m, s.get_maximum_similarity(l[i],l[j]))


    return m    

def between_similarity(bag,key):
    n = len(bag)
    m = 0
    
    for comp in range(1,n):
        if key == comp:
            continue
        for i in bag[key]:
            for j in bag[comp]:
                m = max(m,s.get_maximum_similarity(i,j))
    return m
    
p,labels = g.parse_all()

s.collect_df()


# bag = [[] for x in range(10)]

# for key,result in enumerate(p):
#     bag[int(labels[key])].append(result)


# print "Inner-Similarity"
# for i in range(1,10):
#     print bag[i]
#     print "INNER :",inner_similarity(bag[i])

# print "Between-Similarity"
# for i in range(1,10):
#     print between_similarity(bag,i)
