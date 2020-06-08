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
no_of_lines = 0
doc_wordcount = 0
des_wordcount = 0
jd_kw_file = r"C:\Users\krkc6\PycharmProjects\jobdescription\2_Data_Cleaning_for_online_job_data\jobs_per_line_unique_words\Analyst_test"
appendFile = open(jd_kw_file, 'r', encoding='utf-8')
tf = []
lines = appendFile.readlines()
for line in lines:
    #print(line)
    no_of_lines = no_of_lines+1
    words = line.split(" ")
    for w in words:
        des_wordcount = des_wordcount+1
        tf.append(words.count(w))
    print("Pairs\n" + str(list(zip(words, tf))))
#print("Pairs\n" + str(list(zip(words, tf))))

df = []
#lines1 = appendFile.readlines()
lines2 = str(lines)
words1 = lines2.split(" ")
for ww in words1:
    doc_wordcount = doc_wordcount+1
    df.append(words1.count(ww))
#print("Pairs\n" + str(list(zip(words1, df))))

idf = np.log(no_of_lines/(df[1]+1))
print(idf)