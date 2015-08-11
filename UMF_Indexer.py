import pandas as pd
import os
import urllib
import urllib2

from sets import Set
from boilerpipe.extract import Extractor

from elasticsearch import Elasticsearch


class UMF_Indexer:
    DOCUMENT_LIST_FILENAME = "docList.csv"
    
    INDEX_QUERY_NAME = 'umf_query'
    INDEX_DOCUMENT_NAME = 'umf_document'
    
    def __init__(self):
        self.es = Elasticsearch([{'host':'localhost','port':9200}])

    # build query vector
    def build_all_query_vector(self,directory):        
        for idx,f in enumerate(os.listdir(directory)):
            if f.endswith('.csv'):
                self.build_qd_vector(directory + '/' +f)
                print "FILE:",f, "has been Done"

    # build document vector
    def build_query_vector(self,filename):
        bucket = filename.split('_')
        name = bucket[0]
        age = bucket[2]
        question = bucket[3]
        
        data = pd.read_csv(open(filename),sep='\t',names=['query','document','time'])

        vector = pd.DataFrame()

        querySet = []

        for index,entry in data.iterrows():
            q = entry['query']
            q = q.replace('\'','')
            q = q.replace(']','')
            q = q.replace('[','')
            q = q.replace(',','')
            q = q.replace('\"','')
            
            if not q in querySet:
                querySet.append(q)
            
            # d = entry['document']

            # if not d in docSet:
            #     if ('http' in d) or ('https' in d):
            #         docSet.append(entry['document'])

            
        # for entry in docSet:
        #     document = self.getDocumentFromURL(entry)

        

        

    # Processing a local file for indexing into Elasticsearch.
    # It reads
    def processFile(self,filename):
        ID = filename.split('.')[0]
        cnt = 0
        question = ID.split('_')[3]

        data = pd.read_csv(open(filename),sep='\t',names=['query','document','time'])
        
        querySet = []
        docSet = []
        print "Processing file:",filename

        # Remove duplicate queries and documents
        for index,entry in data.iterrows():
            q = entry['query']
            q = q.replace('\'','')
            q = q.replace(']','')
            q = q.replace('[','')
            q = q.replace(',','')
            q = q.replace('\"','')
            if not q in querySet:
                querySet.append(q)
            
            d = entry['document']

            if not d in docSet:
                if ('http' in d) or ('https' in d):
                    docSet.append(entry['document'])

        # Index query
        for entry in querySet:
            docin = { 'id' : ID + '_' + str(cnt), 'query' : entry, 'question': question}
            self.queryIndexing(docin)
            cnt = cnt + 1

        # Index document
        cnt = 0
        for entry in docSet:
            document = self.getDocumentFromURL(entry)
            docin = { 'id' : ID + '_' + str(cnt), 'document' : document, 'question' : question}
            self.documentIndexing(docin)
            cnt = cnt + 1

    def processAllExperiments(self,directory):
        for idx,f in enumerate(os.listdir(directory)):
            if f.endswith('.csv'):
                self.processFile(directory + '/' +f)
                print "FILE:",f, "has been Done"

    # Document that each user read is saved in form of URL,
    # this function read all files in the local directory(variable 'directory'),
    # and return the set of URLs witout duplicates. 
    def extractDocumentUrl(self,directory):
        urlList = Set()

        for f in os.listdir(directory):
            if f.endswith('.csv'):
                data = pd.read_csv(open(directory+'/'+f),sep='\t',names=['query','document','time'])
                s = Set(data['document'].tolist())
                urlList = urlList | s

        return urlList

    # Getting Body Text extracted from Web page
    # Return the extracted document
    def getDocumentFromURL(self,url):
        print 'searching...',url
        extractor = Extractor(extractor='ArticleExtractor',url=url)
        processed_plaintext = extractor.getText()

        return processed_plaintext

    # Query Indexing to Elasticsearch
    # @param : docin {'id': id, 'query' : query, 'question' : question}
    def queryIndexing(self,docin):
        print "Query Indexing... ",docin
        res = self.es.index(index=UMF_Indexer.INDEX_QUERY_NAME + '_bm25',doc_type='query',id=docin['id'],body=docin)
        print "Query Indexing(bm25) :",res['created']
        res = self.es.index(index=UMF_Indexer.INDEX_QUERY_NAME + '_ib',doc_type='query',id=docin['id'],body=docin)
        print "Query Indexing(ib) :",res['created']
        res = self.es.index(index=UMF_Indexer.INDEX_QUERY_NAME + '_lmd',doc_type='query',id=docin['id'],body=docin)
        print "Query Indexing(lmd) :",res['created']
        res = self.es.index(index=UMF_Indexer.INDEX_QUERY_NAME + '_lmj',doc_type='query',id=docin['id'],body=docin)
        print "Query Indexing(lmj) :",res['created']
        res = self.es.index(index=UMF_Indexer.INDEX_QUERY_NAME + '_tfidf',doc_type='query',id=docin['id'],body=docin)
        print "Query Indexing(tfidf) :",res['created']
        res = self.es.index(index=UMF_Indexer.INDEX_QUERY_NAME + '_dfr',doc_type='query',id=docin['id'],body=docin)
        print "Query Indexing(dfr) :",res['created']
                            
        res = self.es.index(index=UMF_Indexer.INDEX_QUERY_NAME + '_ngram',doc_type='query',id=docin['id'],body=docin)
        print "Query Indexing(ngram) :",res['created']

    # Document Indexing to Elasticsearch
    # @param : docin {'id': id, 'document' : document, 'question' : question}
    def documentIndexing(self,docin):
        print "Document Indexing... ",docin
        res = self.es.index(index=UMF_Indexer.INDEX_DOCUMENT_NAME + '_bm25',doc_type='document',id=docin['id'],body=docin)
        print "Document Indexing(bm25) :",res['created']
        res = self.es.index(index=UMF_Indexer.INDEX_DOCUMENT_NAME + '_ib',doc_type='document',id=docin['id'],body=docin)
        print "Document Indexing(ib) :",res['created']
        res = self.es.index(index=UMF_Indexer.INDEX_DOCUMENT_NAME + '_lmd',doc_type='document',id=docin['id'],body=docin)
        print "Document Indexing(lmd) :",res['created']
        res = self.es.index(index=UMF_Indexer.INDEX_DOCUMENT_NAME + '_lmj',doc_type='document',id=docin['id'],body=docin)
        print "Document Indexing(lmj) :",res['created']
        res = self.es.index(index=UMF_Indexer.INDEX_DOCUMENT_NAME + '_tfidf',doc_type='document',id=docin['id'],body=docin)
        print "Document Indexing(tfidf) :",res['created']
        res = self.es.index(index=UMF_Indexer.INDEX_DOCUMENT_NAME + '_dfr',doc_type='document',id=docin['id'],body=docin)
        print "Document Indexing(dfr) :",res['created']
        res = self.es.index(index=UMF_Indexer.INDEX_DOCUMENT_NAME + '_ngram',doc_type='document',id=docin['id'],body=docin)
        print "Document Indexing(ngram) :",res['created']

