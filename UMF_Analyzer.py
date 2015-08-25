from elasticsearch import Elasticsearch
from sets import Set

import pandas as pd
import os
import math

class UMF_Analyzer:

    def __init__(self):
        self.es = Elasticsearch([{'host':'localhost', 'port': 9200}])
        self.scheme = ['bm25','ib','lmd','lmj','ngram','tfidf','dfr']
        self.umf_query = 'umf_query'
        self.umf_document = 'umf_document'
        self.docMap = pd.read_csv(open('doc_map.csv'),sep='\t',index_col=False)

    # Build Similarity vector between all pairs of users
    def build_similarity_vector(self,directory):
        labels = []
        ids = []
        
        for filename in os.listdir(directory):
            labels.append(filename.split('_')[3].split('.')[0])
            ids.append(filename.split('.')[0])
            
        qVector = {}
        for s in self.scheme:
            qVector[s] = pd.DataFrame()

            
        # Build Query Similarity Vector
        cnt = 0
        for filename1 in os.listdir(directory):
            data1 = pd.read_csv(open(directory + '/'+filename1),sep='\t',names=['query','document','time'])
            pivot_id = filename1.split('.')[0]
            v={}
    
            for s in self.scheme:
                v[s] = []
                
            for filename2 in os.listdir(directory):
                data2 = pd.read_csv(open(directory + '/' + filename2),sep='\t',names=['query','document','time'])
                sim = self.calculate_query_similarities(data1['query'],data2['query'])
                #print "similarity:",sim
    
                for s in self.scheme:
                    v[s].append(sim[s])
            
            for s in self.scheme:
                temp = {}
                for idx,l in enumerate(ids):
                    temp[l] = v[s][idx]

                a = pd.DataFrame(temp,index=[pivot_id],columns=ids)
                qVector[s] = qVector[s].append(a)

            cnt = cnt + 1
                                               
        return qVector
        
        
        #print pd.DataFrame(v)
        # vectors = {}
        # for s in self.scheme:
        #     vectors[s] = pd.DataFrame()
        #     for i in v:
        #         temp = []
        #         for j in i:
        #             temp.append(j[s])
        #         vectors[s] = vectors[s].append(pd.DataFrame(temp))
        #         print temp

        # print 'test'
        # print vectors['ngram']
                
                    

                
        
       
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

    def display_analysis(self):
        print "############Query Inner Similarity#############"
        scores = self.inner_similarity_query('data')
        for i in range(9):
            print "######################Q",i+1,"#################"
            for s in self.scheme:
                print s,":",scores[i][s]

        print "############Document Inner Similarity#############"
        scores = self.inner_similarity_document('data')
        for i in range(9):
            print "Q",i+1,":",scores[i]
        

    def inner_similarity_query(self,directory,display=False):
        l = []
        for i in range(9):
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
                    if display:
                        print Sim_kj

            for s in self.scheme:
                avg[s] = avg[s]/cnt

            l.append(avg)
        return l

    def inner_similarity_document(self,directory,display=False):
        l = []
        for i in range(9):
            files = []
            avg = 0
            cnt = 0
            
            for filename in os.listdir(directory):
                if filename.split('_')[3] == str(i+1) + '.csv':
                    files.append(filename)
                    
            for k in range(len(files)-1):
                dSet1 = pd.read_csv(open(directory + '/' + files[k]),sep='\t',names=['query','document','time'])
                for j in range(k+1,len(files)):
                    dSet2 = pd.read_csv(open(directory + '/' + files[j]),sep='\t',names=['query','document','time'])
                    Sim_kj = self.calculate_document_similarities(dSet1['document'],dSet2['document'])
                    
                    avg = avg+Sim_kj
                    cnt = cnt + 1
                    if display:
                        print Sim_kj
    
            l.append(avg/cnt)
        return l

    def outer_similairty_document(self,directory,display=False):
        for i in range(9):
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
                    if display:
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
        return avg

    def calculate_cluster_document_similarity(self,directory, num1,num2):
        avg = 0
        files1 = []
        files2 = []
        cnt = 0

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
                avg = avg + Sim_ij
                cnt = cnt+1
    
        return avg/cnt

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
        # from goose import Goose
        # g = Goose()
        # article = g.extract(url=url)
        # text = ''.join([i if ord(i) < 128 else '' for i in article.cleaned_text])
        # return text
        
        for idx,entry in self.docMap.iterrows():
            if entry['key'] == url:
                if type(entry['value']) == float:
                    return None
                return entry['value']
            
    def getDocumentIDFromURL(self,url):
        for idx,entry in self.docMap.iterrows():
            if entry['key'] == url:
                return entry['id']

    def getDocumentIDFromDocument(self,document):
        for idx,entry in self.docMap.iterrows():
            if entry['value'] == document:
                return entry['id']

    def document_preprocess(self,dSet):
        dSet = self.remove_duplicates(dSet) # remove duplicates

        if 'https://google.com/' in dSet:
            dSett = dSet.remove('https://google.com/')
        if 'http://google.com/' in dSet:
            dSet.remove('http://google.com/')
        if 'http://www.google.com/' in dSet:
            dSet.remove('http://www.google.com/')
        if 'https://www.google.com/' in dSet:
            dSet.remove('https://www.google.com/')
        if 'http://www.google.co.kr/' in dSet:
            dSet.remove('http://www.google.co.kr/')
        if 'http://www.google.com/webhp?hl=en' in dSet:
            dSet.remove('http://www.google.com/webhp?hl=en')
        if 'about:blank' in dSet:
            dSet.remove('about:blank')

        if 'google.com' in dSet:
            dSet.remove('google.com')

        return dSet
    

    
    def calculate_document_similarities(self,dSet1,dSet2):
        dSet1 = self.document_preprocess(dSet1)
        dSet2 = self.document_preprocess(dSet2)

        score = 0
        for d1 in dSet1:
            for d2 in dSet2:
                rD1 = self.getDocumentFromURL(d1)
                rD2 = self.getDocumentFromURL(d2)

                if rD2 == None or rD1 == None:
                    continue

                score = score + self.calculate_document_similarity(rD1,rD2)

        cnt = len(dSet1) * len(dSet2)

        return score/cnt
                

    def calculate_document_similarity(self,d1,d2):
        ID1 = self.getDocumentIDFromDocument(d1)
        ID2 = self.getDocumentIDFromDocument(d2)

        if ID1 == ID2:
            return 1.0

        score = 0
        res = self.es.mlt(index=self.umf_document+'_bm25',doc_type='document',id=ID1,search_size=200)
        for entry in res['hits']['hits']:
            if entry['_id'] == ID2:
                return entry['_score']
        return 0.0
