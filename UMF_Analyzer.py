from elasticsearch import Elasticsearch
from sets import Set

from boilerpipe.extract import Extractor


class UMF_Analyzer:
    def __init__(self):
        self.es = Elasticsearch([{'host':'localhost', 'port': 9200}])
        self.scheme = ['bm25','ib','lmd','lmj','ngram','tfidf','dfr']
        self.umf_query = 'umf_query'
        self.umf_document = 'umf_document'
   
    # remove duplicates
    def remove_duplicates(self,queries):
        return Set(queries)
    
    # Query Refinement
    def query_refine(self,q):
        q = q.replace('\'','')
        q = q.replace(']','')
        q = q.replace('[','')
        q = q.replace(',','')
        q = q.replace('\"','')
        return q

    def inner_similarity_query(self):
        pass
        
    def inner_similairty_document(self):
        pass


    # This function calculates similarities between two sets of queries.
    # 'function calculate_query_similarity' is called
    def calculate_query_similarities(self,qSet1,qSet2):
        qSet1 = self.remove_duplicates(qSet1)
        qSet2 = self.remove_duplicates(qSet2)

        scores = {}
        for s in self.scheme:
            scores[s] = 0

        for q1 in qSet1:
            for q2 in qSet2:
                rQ1 = self.query_refine(q1)
                rQ2 = self.query_refine(q2)
                score = self.calculate_query_similarity(rQ1,rQ2)
                for s in self.scheme:
                    scores[s] = scores[s] + score[s]
            
        return scores
                                     
    # This function calculates similarity between two queries
    def calculate_query_similarity(self,q1,q2):
        scores = {}

        for s in self.scheme:
            scores[s] = 0
            analyzer = 'my_' + s + '_analyzer'
            content = q1.replace(r"/",",")

            res = self.es.search(index=self.umf_query+ '_' + s, q=content,doc_type='query',analyzer=analyzer,size=4000)
            
            for entry in res['hits']['hits']:
                if q2 == entry['_source']['query']:
                    scores[s] = entry['_score']
                    break

        return scores

    # Getting Body Text extracted from Web page
    # Return the extracted document
    def getDocumentFromURL(self,url):
        extractor = Extractor(extractor='DefaultExtractor',url=url)
        processed_plaintext = extractor.getText()

        return processed_plaintext


    def calculate_document_similarities(self,dSet1,dSet2):
        pass

    def calculate_document_similarity(self,d1,d2):
        scores = {}

        for s in self.scheme:
            scores[s] = 0
            analyzer = 'my_' + s + '_analyzer'
            content = d1.replace(r"/",",")
            
            res = self.es.search(index=self.umf_document+ '_' + s, q=content,doc_type='document',analyzer=analyzer,size = 4000)

            for entry in res['hits']['hits']:
                if d2 == entry['_source']['document']:
                    scores[s] = entry['_score']
                    break
