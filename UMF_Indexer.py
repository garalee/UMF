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
        self.docMap = pd.read_csv(open('doc_map.csv'),sep='\t',index_col=False)

    # Building Document Map
    def build_document_map(self,directory):
        doc_pack = []
        for f in os.listdir(directory):
            data = pd.read_csv(open(directory+'/'+f),sep='\t',names=['query','document','time'])
            for d in data['document']:
                if not d in doc_pack:
                    doc_pack.append(d)

        docMap = pd.DataFrame()

        for d in doc_pack:
            content = self.getDocumentFromURL(d)
            content = content.replace(r"/",",")
            docMap = docMap.append(pd.DataFrame({'key' : [d], 'value' : [content.encode('utf-8')]}))

        docMap.to_csv('doc_test.csv',sep='\t',columns=['key','value'],index=False,encoding='utf-8')
        return docMap

    # Query Refinement
    def query_refine(self,q):
        q = q.replace('\'','')
        q = q.replace(']','')
        q = q.replace('[','')
        q = q.replace(',','')
        q = q.replace('\"','')
        return q

    def document_refine(self,d):
        d = d.replace(r"/",",")
        d = d.replace("\t"," ")
        return d
        

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
            q = self.query_refine(entry['query'])
            q = q.replace(r"/",",")
            if not q in querySet:
                querySet.append(q)
            
            d = entry['document']

            # Duplicates not checked
            if not d in docSet:
                if ('http' in d) or ('https' in d):
                    docSet.append(entry['document'])

        # Index query
        for entry in querySet:
            docin = { 'id' : ID + '_' + str(cnt), 'query' : entry, 'question': question}
            self.queryIndexing(docin)
            cnt = cnt + 1
        
        # Index document
        docMap = pd.DataFrame()
        cnt = 0
        for entry in docSet:
            document = self.getDocumentFromURL(entry)
            document = self.document_refine(document)
            docin = { 'id' : ID + '_' + str(cnt), 'document' : document, 'question' : question}
            self.documentIndexing(docin)
            docMap = docMap.append(pd.DataFrame({'id' : [docin['id']], 'key':[entry],'value': [document]}))
            cnt = cnt + 1
        return docMap
            

    def processAllExperiments(self,directory):
        docMap = pd.DataFrame()
        for idx,f in enumerate(os.listdir(directory)):
            if f.endswith('.csv'):
                docMap = docMap.append(self.processFile(directory + '/' +f))
                print "FILE:",f, "Done"
        docMap.to_csv('doc_map.csv',sep='\t',columns=['id','key','value'],index=False,encoding='utf-8')

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
        
        for idx,entry in self.docMap.iterrows():
            if entry['key'] == url:
                return entry['value']

        # from goose import Goose
        # g = Goose()
        # article = g.extract(url=url)
        # text = ''.join([i if ord(i) < 128 else '' for i in article.cleaned_text])
        # return text
    

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
