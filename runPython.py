import pandas as pd
from bs4 import BeautifulSoup
import urllib2


import UMF_Indexer
import UMF_Analyzer

if __name__ == "__main__":
    indexer = UMF_Indexer.UMF_Indexer()
    analyzer = UMF_Analyzer.UMF_Analyzer()

    #analyzer.inner_similarity_query('data')
    # indexer.build_document_map('data')
    # print analyzer.docMap['value']
    # indexer.processAllExperiments('data')
    q_score = analyzer.calculate_cluster_query_similarity('data',1,2)
    d_score = analyzer.calculate_cluster_document_similarity('data',1,2)

    print "Q Score:",q_score
    print "D Score:",d_score

    # data1 = pd.read_csv('data/CMS_M_25_2.csv',sep='\t',names=['query','document','time'])
    # data2 = pd.read_csv('data/CSD_M_34_2.csv',sep='\t',names=['query','document','time'])
    
    # score = analyzer.calculate_query_similarities(data1['query'],data2['query'])
    # print "SCORE :",score

    # score = analyzer.calculate_document_similarities(data1['document'],data2['document'])
    # print "Scores :",score

    
