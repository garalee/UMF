import pandas as pd
from bs4 import BeautifulSoup
import urllib2


import UMF_Indexer
import UMF_Analyzer

if __name__ == "__main__":
    indexer = UMF_Indexer.UMF_Indexer()
    analyzer = UMF_Analyzer.UMF_Analyzer()


    indexer.build_document_map('data')

    # indexer.processAllExperiments('data')

    # data1 = pd.read_csv('data/CMS_M_25_2.csv',sep='\t',names=['query','document','time'])
    # data2 = pd.read_csv('data/CSD_M_34_2.csv',sep='\t',names=['query','document','time'])
    
    # score = analyzer.calculate_query_similarities(data1['query'],data2['query'])
    # print "SCORE :",score

    # score = analyzer.calculate_document_similarities(data1['document'],data2['document'])
    # print "Scores :",score

    


    # print "URL1:",data1['document'][0]
    # print "URL2:",data2['document'][1]

    # from goose import Goose

    # url = 'https://answers.yahoo.com/question/index?qid=20060807064501AAoPdPd'
    # g = Goose()
    # article = g.extract(url=url)
    # print article.cleaned_text

    # print "DOC1 :",doc1
    # print "DOC2 :",doc2

    # page = urllib2.urlopen('https://answers.yahoo.com/question/index?qid=20060807064501AAoPdPd').read()
    # soup = BeautifulSoup(page)
    # print "TYPE:",type(soup)
    # print "DOC1:",soup.find_all('b')
    
    # page = urllib2.urlopen(data2['document'][0]).read()
    # soup = BeautifulSoup(page)
    # print "DOC2:",soup.get_text()
    
    # print "DOC SCORE :",analyzer.calculate_document_similarity(doc1,doc2)
