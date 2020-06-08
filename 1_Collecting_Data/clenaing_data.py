import numpy as np
import pandas as pd
# For visualizations
import matplotlib.pyplot as plt
# For regular expressions
import re
# For handling string
import string
# For performing mathematical operations
import math
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

stop_words = stopwords.words('english')

newStopWords = ['apply','now','new','opportunity','not','to','be','missed']
#stop_words.append(newStopWords)
#print(stop_words)
jd_kw_file = r"C:\Users\krkc6\Desktop\stop_word"
appendFile = open(jd_kw_file, 'w', encoding='utf-8')
path = r"C:\Users\krkc6\Desktop\reed_uk.csv"

df=pd.read_csv(path)
print("Shape of data=>",df.shape)

df=df[['job_title','job_description']]
print("Shape of data=>",df.shape)
#print(df.head(5))

#print(df.isnull().sum())
df['job_description']=df['job_description'].apply(lambda x: x.lower())
df['job_description']=df['job_description'].apply(lambda x: re.sub('\w*\d\w*','', x))
df['job_description']=df['job_description'].apply(lambda x: re.sub('[%s]' % re.escape(string.punctuation), '', x))
for i in range(len(df['job_description'])):
    line = df['job_description'][i].split(" ")

    #df['stop_cleaned'] = df['some'].apply(lambda x: ' '.join([word for word in line if (word not in stop_words==True)]))

    for word in line:
        if word not in stop_words:
            appendFile.write(" " + word)
    appendFile.write("\n")
appendFile.close()

tf = [] * 50000
for j in range(len(df['job_description'])):
    line = df['job_description'][j]
    words = line.split(" ")
    for w in words:
        tf.append(words.count(w))

print(tf[1])

#print(df['stop_cleaned'])
