#!/usr/bin/python
import warnings
warnings.filterwarnings("ignore")
import shutil
import math
import re
import pandas as pd
from collections import Counter
import queue as Q
import csv
from feature import clf,count_vect
from preprocessing import TextPreprocessor 

columns = shutil.get_terminal_size().columns
WORD = re.compile(r"\w+")
postfiles = ['AI','AImeta','ComputerGraphic','ComputerGraphicmeta','CS','CSmeta','DataScience','DataSciencemeta']

class Post(object):
    def __init__(self, priority, description):
        self.priority = priority
        self.description = description
        return

q = Q.PriorityQueue()
q2 = Q.PriorityQueue()
def get_cosine(vec1, vec2):
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])

    sum1 = sum([vec1[x] ** 2 for x in list(vec1.keys())])
    sum2 = sum([vec2[x] ** 2 for x in list(vec2.keys())])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator

def text_to_vector(text):
    words = WORD.findall(text)
    return Counter(words)

text2 = "Hint: Hamiltonian Cycle is $NP$-Complete."
print("Query  : ".center(columns),text2.center(columns))
print("These are the top 5 search results")
print("*******************************************************************************************************************************\n")

xml_data = open( 'query.csv','w',newline='',encoding='utf-8')
csvwriter = csv.writer(xml_data)
col_names = ['Query']
csvwriter.writerow(col_names)
data = []
data.append(text2)
csvwriter.writerow(data)
xml_data.close()
data_agg = pd.read_csv('query.csv')
data_agg_processed = TextPreprocessor(n_jobs=-1).transform(data_agg,'Query')
data_agg_processed.to_csv('query.csv',encoding='utf-8',index=False)
df=pd.read_csv('query.csv',header=None)
df.T.rename(columns={0:'Query', 1: 'processed_Query'})
text2 = df[1][1]
vector2 = text_to_vector(text2)

tag = clf.predict(count_vect.transform([text2]))
count = 0
for each_file in postfiles:
    df=pd.read_csv('csv/'+ each_file +'.csv',header=None)
    df.T.rename(columns={0:'Id',1:'Text',2: 'Topic',3: "processed_Text"})
    len = df.shape[0]
    count+=len
    for i in range (1,len):
        text1 = str(df[3][i])
        vector1 = text_to_vector(text1)
        cosine = get_cosine(vector1, vector2) 
        q.put((cosine*-1, df[1][i]))
print("Nodes explored :",count,"\n")
for _ in range(0,5):
    next_level = q.get()
    print(next_level[1]) 
    print("*******************************************************************************************************************************\n")

count = 0
for each_file in tag:
    df=pd.read_csv('csv/'+ each_file +'.csv',header=None)
    df.T.rename(columns={0:'Id',1:'Text',2: 'Topic',3: "processed_Text"})
    len = df.shape[0]
    count+=len
    for i in range (1,len):
        text1 = str(df[3][i])
        vector1 = text_to_vector(text1)
        cosine = get_cosine(vector1, vector2) + 0.0001
        q2.put((1/cosine, df[1][i]))
print("Nodes explored :",count,"\n")
for _ in range(0,5):
    next_level = q2.get()
    print(next_level[1]) 
    print("*******************************************************************************************************************************\n")
