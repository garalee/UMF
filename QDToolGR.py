import pandas as pd
import numpy as np
import math
from elasticsearch import Elasticsearch

import os

from pandas import DataFrame

DF_FILE = "DF_FILE.csv"


# Made By Garam Laboratory


# This class is made on purpose that parses and analyzes dataset(query and document)
# extracted from the application "rightnow".
# The format of dataset will be .csv
# in form of "query" \t "url of document" \t "time"
# ,where "time" stands for the time it takes to read the document


class QDToolGR:
    def __init__(self):
        self.es = Elasticsearch([{'host':'localhost','port':9200}])
        
    # This function parses the dataset
    # the separator is '\t', and sections are "query", "document", and "time"
    #
    # Also, it parses the filename. Filename contains the name of user,
    # sex, age,and question numbers
    #
    # return the tuple (name,sex,age,questions,dataset) 
    def parse(self,filename):
        dataset = pd.read_csv(open(filename),sep='\t',names=['query','document','time'])
        # parse filename
        s = filename.split('.')[0]
        s = s.split('_')
        name = s[0]
        sex = s[1]
        age = s[2]
        questions = s[3]
            
        return (name,sex,age,questions,dataset)


    # This function extracts quries only from the dataset.
    # Returns "Bag of Words" 
    def extract_queries(self):
        bow = []
        
        for i in dataset['query']:
            if not i in bow:
                bow.append(i)

        return bow


    # This function refines a list query, that is, convert string form of queries into type of array. 
    # Given string form of queries,
    # Returns an array consisting of words
    def refine_queries(self,queries):
        r = []
        i = 0
        for q in queries:
            if type(q) == float:
                continue
            
            q = q[1:]
            q = q[:-2]
            r.append("")
            for k in q.split(','):
                r[i] = r[i] + k

            r[i] = r[i].replace("\'","")
            r[i] = r[i].replace("\"","")
            i = i + 1
        return r
    
    # This function extracts documents corresponding to the quries in bag of words.
    # Returns map whose key is query, and value is list of documents.
    def extract_documentsurl(self,bow, dataset):
        m = {}
        for key,i in enumerate(bow):
            m[key] = dataset[dataset['query'] == i]['document']

        return m

    def parse_all(self):
        p = []
        dirs = os.listdir(".")
        labels = []
        for i in dirs:
            if not i.split(".")[1] == 'csv':
                continue
                
            if i.split(".")[0] == 'DF_FILE' or i.split(".")[0] == 'df_test':
                continue
            
            (name,sex,age,questions,dataset) = self.parse(i)
            
            labels.append(questions)
            qs = self.extract_queries(dataset)
            qs = self.refine_queries(qs)
            p.append(qs)
            
        return p,labels

    def test(self,filename = 'HWJ_M_30_3_5_9.csv'):
        name,sex,age,questions,dataset = self.parse(filename)
        queries = self.extract_queries(dataset)
        return self.refine_queries(queries)


    # Index all quries and documents encountered in this experiment
    def doIndex(self,content,t):
        docin = {'content' : content,
                 'type' : t
                 }

        self.es.index(index="bm25",doc_type="article",body=docin)
        self.es.index(index="dfr",doc_type="article",body=docin)
        self.es.index(index="ib",doc_type="article",body=docin)
        self.es.index(index="lmd",doc_type="article",body=docin)
        self.es.index(index="lmj",doc_type="article",body=docin)
        self.es.index(index="ngram",doc_type="article",body=docin)
        self.es.index(index="tfidf",doc_type="article",body=docin)

    def queryIndex(self):
        os.chdir("data")
        for file in glob.glob("*.csv"):
            data = pd.read_csv(open(file),sep='\t',names=['query','document','time'])
            for data['query']
            
