import pandas as pd

import UMF_Indexer
import UMF_Analyzer

if __name__ == "__main__":
    indexer = UMF_Indexer.UMF_Indexer()
    analyzer = UMF_Analyzer.UMF_Analyzer()

    data1 = pd.read_csv('data/CMS_M_25_2.csv',sep='\t',names=['query','document','time'])
    data2 = pd.read_csv('data/CSD_M_34_2.csv',sep='\t',names=['query','document','time'])

    # print "SCORE :",analyzer.calculate_query_similarities(data1['query'],data2['query'])
    print "DOC1 :",data1['document'][0]
    print "DOC2 :",data2['document'][0]
    print "DOC SCORE :",analyzer.calculate_document_similarity(data1['document'][0],data2['document'][0])
