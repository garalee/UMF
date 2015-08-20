import pandas as pd
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

    # print data1['document'][0]
    # print data2['document'][0]
    
    # doc1 = analyzer.getDocumentFromURL(data1['document'][0])
    # doc2 = analyzer.getDocumentFromURL(data2['document'][0])

    # ID1 = analyzer.getDocumentIDFromDocument(doc1)
    # ID2 = analyzer.getDocumentIDFromDocument(doc2)

    # res = analyzer.es.mlt(index='umf_document_bm25',doc_type='document',id=ID1,search_size=200)
    
    # for entry in res['hits']['hits']:
    #     if entry['_id'] == ID2:
    #         print entry['_score']
            

    
    # score = analyzer.calculate_query_similarities(data1['query'],data2['query'])
    # print "SCORE :",score

    # score = analyzer.calculate_document_similarities(data1['document'],data2['document'])
    # print "Scores :",score

    
    
