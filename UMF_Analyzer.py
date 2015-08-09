from elasticsearch import Elasticsearch


class UMF_Analyzer:
    def __init__(self):
        self.es = Elasticsearch([{'host':'localhost', 'port': 9200}])
        
    def inner_similarity_query(self):
        pass
        

    def inner_similairty_document(self):
        pass
