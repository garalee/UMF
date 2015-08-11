from elasticsearch import Elasticsearch


class UMF_Analyzer:
    def __init__(self):
        self.es = Elasticsearch([{'host':'localhost', 'port': 9200}])
        self.scheme = ['bm25','ib','lmd','lmj','ngram','tfidf','dfr']
        self.umf_query = 'umf_query'
        self.umf_document = 'umf_document'
        
    def inner_similarity_query(self):
        pass
        
    def inner_similairty_document(self):
        pass

    def calculate_query_similarities(self,qSet1,qSet2):
        for q in qSet1:
            pass

        for q in qSet2:
            pass
        
    def calculate_document_similarity(self,dSet1,dSet2):
        pass

    
    def calculate_query_similarity(self,q1,q2):
        for s in self.scheme:
            analyzer = 'my_' + s + '_analyzer'
            content = q1.replace(r"/",",")
            res = self.es.search(index=self.umf_query+ '_' + s, q=content,doc_type='query',analyzer=analyzer,size=4000)
            
            for entry in res['hits']['hits']:
                for e in entry:
                    print e
            
