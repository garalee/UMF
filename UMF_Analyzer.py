from elasticsearch import Elasticsearch
from sets import Set

import pandas as pd
import os

class UMF_Analyzer:
    def __init__(self):
        self.es = Elasticsearch([{'host':'localhost', 'port': 9200}])
        self.scheme = ['bm25','ib','lmd','lmj','ngram','tfidf','dfr']
        self.umf_query = 'umf_query'
        self.umf_document = 'umf_document'
        self.docMap = pd.read_csv(open('doc_test.csv'),sep='\t',names=['key','value'],index_col=False)
   
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

    def inner_similarity_query(self,directory):
        for i in range(9):
            print "################################################",i+1,"Question #####"
            files = []
            avg = {}
            cnt = 0
            for s in self.scheme:
                avg[s] = 0

            for filename in os.listdir(directory):
                if filename.split('_')[3] == str(i+1) + '.csv':
                    files.append(filename)
    
            for k in range(len(files)-1):
                qSet1 = pd.read_csv(open(directory + '/' + files[k]),sep='\t',names=['query','document','time'])
                for j in range(k+1,len(files)):
                    qSet2 = pd.read_csv(open(directory + '/' +files[j]),sep='\t',names=['query','document','time'])
                    Sim_kj = self.calculate_query_similarities(qSet1['query'],qSet2['query'])
                    
                    for s in self.scheme:
                        avg[s] = avg[s] + Sim_kj[s]
                    cnt = cnt + 1
                    print Sim_kj

            for s in self.scheme:
                avg[s] = avg[s]/cnt
            print "Average:",avg
        
    def outer_similairty_document(self,directory):
        for i in range(9):
            print "################################################",i+1,"Question #####"
            files1 = []
            files2 = []
            cnt = 0
            avg = {}

            for s in self.scheme:
                avg[s] = 0

            for filename in os.listdir(directory):
                if filename.split('_')[3] == str(i+1) + '.csv':
                    files1.append(filename)

            for filename in os.listdir(directory):
                if not filename.split('_')[3] == str(i+1) + '.csv':
                    files2.append(filename)

            


            for k in range(len(files) -1):
                qSet1 = pd.read_csv(open(directory + '/' + files[k]),sep='\t',names=['query','document','time'])
                for j in range(k+1,len(files)):
                    qSet2 = pd.read_csv(open(directory + '/' +files[j]),sep='\t',names=['query','document','time'])
                    Sim_kj = self.calculate_query_similarities(qSet1['query'],qSet2['query'])
                    
                    for s in self.scheme:
                        avg[s] = avg[s] + Sim_kj[s]
                    cnt = cnt + 1    
                    print Sim_kj

            for s in self.scheme:
                avg[s] = avg[s]/cnt
            print "Average:",avg
            
            
    def calculate_cluster_query_similarity(self,directory, num1,num2):
        avg = {}
        files1 = []
        files2 = []
        cnt = 0

        for s in self.scheme:
            avg[s] = 0

        for filename in os.listdir(directory):
            if filename.split('_')[3] == str(num1) + '.csv':
                files1.append(filename)

        for filename in os.listdir(directory):
            if filename.split('_')[3] == str(num2) + '.csv':
                files2.append(filename)

        for i in range(len(files1) -1):
            qSet1 = pd.read_csv(open(directory + '/' + files1[i]),sep='\t',names=['query','document','time'])
            for j in range(i+1,len(files2)):
                qSet2 = pd.read_csv(open(directory + '/' + files2[j]),sep='\t',names=['query','document','time'])
            
                Sim_ij = self.calculate_query_similarities(qSet1['query'],qSet2['query'])

                for s in self.scheme:
                    avg[s] = avg[s] + Sim_ij[s]
                cnt = cnt+1
        for s in self.scheme:
            avg[s] = avg[s]/cnt
        print "Average:",avg

    
    def calculate_cluster_document_similarity(self,directory, num1,num2):
        avg = {}
        files1 = []
        files2 = []
        cnt = 0

        for s in self.scheme:
            avg[s] = 0

        for filename in os.listdir(directory):
            if filename.split('_')[3] == str(num1) + '.csv':
                files1.append(filename)

        for filename in os.listdir(directory):
            if filename.split('_')[3] == str(num2) + '.csv':
                files2.append(filename)

        for i in range(len(files1) -1):
            qSet1 = pd.read_csv(open(directory + '/' + files1[i]),sep='\t',names=['query','document','time'])
            for j in range(i+1,len(files2)):
                qSet2 = pd.read_csv(open(directory + '/' + files2[j]),sep='\t',names=['query','document','time'])
                Sim_ij = self.calculate_document_similarities(qSet1['document'],qSet2['document'])

                for s in self.scheme:
                    avg[s] = avg[s] + Sim_ij[s]
                cnt = cnt+1
    
        for s in self.scheme:
            avg[s] = avg[s]/cnt
        print "Average:",avg

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

        cnt = len(qSet1) * len(qSet2)
        for s in self.scheme:
            scores[s] = scores[s]/cnt
            
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
        from goose import Goose
        g = Goose()
        article = g.extract(url=url)
        text = ''.join([i if ord(i) < 128 else '' for i in article.cleaned_text])
        return text

    def calculate_document_similarities(self,dSet1,dSet2):
        dSet1 = self.remove_duplicates(dSet1)
        dSet2 = self.remove_duplicates(dSet2)

        scores = {}
        for s in self.scheme:
            scores[s] = 0

        for d1 in dSet1:
            for d2 in dSet2:
                rD1 = self.getDocumentFromURL(d1)
                rD2 = self.getDocumentFromURL(d2)

                print "s1:",rD1
                print "s2:",rD2

                score = self.calculate_document_similarity(rD1,rD2)
                for s in self.scheme:
                    scores[s] = scores[s] + score[s]

        cnt = len(dSet1) * len(dSet2)
        for s in self.scheme:
            scores[s] = scores[s]/cnt

        return scores
                

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

        return scores
