import pandas as pd
import numpy as np
import QDToolGR

import urllib2
import urllib
import json
import ast
import math

from random import randint
import time

import os
import subprocess
# Similarity Calculation Tool From GR
# Made By Garam Laboratory

# This class made for calculating the similarity between queries, documents, or query-document compound

DF_FILE = "DF_v2.3.csv"


class SC:
    qdcompound_alpha = 0.5
    qdcompound_beta = 1-qdcompound_alpha

    def __init__(self):
        self.refresh_counter = 2
        self.refresh_frame = 2

        try:
            f = open(DF_FILE,'r')
            self.tf_table = pd.read_csv(f,sep='\t',names=['query','df'])
        except:
            self.tf_table = pd.DataFrame(columns=['query','df'])
            
    def collect_df(self):
        g = QDToolGR.QDToolGR()
        p,labels = g.parse_all()
        
        for i in range(len(p)):
            for j in p[i]:
                
                if any(self.tf_table['query'] == j):
                    continue
                c = self.get_df_from_web(j)
                n = [{'query':str(j), 'df':str(c)}]
                self.tf_table = self.tf_table.append(n)
                
        self.tf_table.to_csv(DF_FILE,sep='\t',index=False)
                
                
        # self.tf_table.to_csv(DF_FILE,sep='\t',index=False)
    
    # This function extracts the number of document resulted from query parameter, 'query' on google search
    # Return the number of documents in form of string type
    def get_df_from_web(self,query):
        a = subprocess.check_output(['python','spider_gr.py',query])
        c = a.split('\n')[0].split(' ')[0]
        
        n = [{'query':str(query),'df':str(c)}]
        self.tf_table = self.tf_table.append(n)
        self.tf_table.to_csv(DF_FILE,sep='\t',index=False)

        return c

    def get_df_from_table(self,query):
        if any(self.tf_table['query'] == query):
            return unicode(self.tf_table[self.tf_table['query'] == query]['df'].values[0])
        return None
        
    def get_similarity_vector(self,p):
        m = [[0 for i in range(len(p))] for j in range(len(p))]
        
        for i in range(len(p)):
            for j in range(len(p)):
                if i==j:
                    m[i][j] = 0
                    continue
                qs = self.get_maximum_similarity(p[i],p[j])
                m[i][j] = qs

        return m

    def get_maximum_similarity(self,p1,p2):
        m = 0
        for i in p1:
            for j in p2: 
                test = self.get_query_similarity2(i,j)
                m = max(m,test)
        return m        

    # Similarity Caculation Method (Equally-Like)
    def get_query_similarity2(self,q1,q2):
        q1 = q1.split(' ')
        q2 = q2.split(' ')
        
        n1 = len(q1)
        n2 = len(q2)
        m = 0

        for i in q1:
            for j in q2:
                if i is j:
                    m += 1

        return float(m)/(n1+n2)

    # This function calculates query similarity between two queries
    def get_query_similarity(self,q1,q2):
        n1 = self.get_df_from_table(q1)
        n2 = self.get_df_from_table(q2)
        n3 = self.get_df_from_table(str(q1) + ' ' + str(q2))
        if not n3:
            n3 = self.get_df_from_table(str(q2) + ' ' +str(q1))


        if not n1:
            n1 = ""
            #n1 = self.get_df_from_web(q1)
        if not n2:
            n2 = ""
            #n2 = self.get_df_from_web(q2)
        if not n3:
            n3 = ""
            #n3 = self.get_df_from_web(str(q1) + ' ' + str(q2))

            
        # print "n1:",n1,"type:",type(n1)
        # print "n2:",n2,"type:",type(n2)
        # print "n3:",n3,"type:",type(n3)

        nq1 = n1.split(',')
        nq2 = n2.split(',')
        nq3 = n3.split(',')

        exponent = 1
        n1 = 0
        n2 = 0
        n3 = 0
        n = 0
        
        for i in reversed(range(len(nq1)-1)):
            n1 = n1 + long(nq1[i])*exponent
            exponent = exponent * 1000
            
        exponent = 1
        for i in reversed(range(len(nq2)-1)):
            n2 = n2 + long(nq2[i])*exponent
            exponent = exponent * 1000

        exponent = 1
    
        if type(nq3) == int:
            n3 = 0
        else:
            for i in reversed(range(len(nq3)-1)):
                n3 = n3 + long(nq3[i])*exponent
                exponent = exponent * 1000

        #print "query similarity : Q1: ",q1, "Q2:",q2," SIMILARITY:", float(n3)/(n1+n2)
            
        return float(n3)/(n1+n2)
                
    def get_document_similarity(self,d1,d2):
        pass

    def get_qdcompound_similarity(self):
        pass
