import pandas as pd
from collections import defaultdict
import os
import re

def remove_filesIfolder():
    import os, shutil
    folder = r"C:\Users\krkc6\Desktop\cate"

    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
remove_filesIfolder()

df = pd.read_csv(r"C:\Users\krkc6\Desktop\reed_uk.csv")

#print(df)



import nltk
import pandas as pd
import re
from nltk.tokenize import word_tokenize
import io
from nltk.corpus import stopwords

stop_words = set(stopwords.words('english'))

#print(stop_words)

#print(len(stop_words))
for i, a in enumerate(df.iterrows()):
    # print(a[1]["job_title"])
    jd = a[1]["category"]
    # job_desc = job_desc + jd
    job_title = a[1]["job_description"]
    # job_title_cleaned = job_title.replace("/" , "_").replace(" ", "_")
    #print(jd)
    #print(job_title)
    with open(r"C:\Users\krkc6\Desktop\cate\type  "+jd, "a", encoding='utf-8') as ff:
        ff.write(job_title+"\n")
        ff.write("\n")



def jdfile_to_kws_file(jdfile_path, jd_kw_file):
    jdfile = open(jdfile_path , "r", encoding='utf-8')

    lines = jdfile.readlines()  # Use this to read file content as a stream:
    #print(lines)
    appendFile = open(jd_kw_file, 'a', encoding='utf-8')
    #print(type(lines))

    for line in lines:
        #print(line)
        words = line.split(" ")
        for r in words:
            if not r in stop_words:
                appendFile.write(" " + r)

        appendFile.write("\n")
    appendFile.close()


jdfile_to_kws_file(
    r"C:\Users\krkc6\Desktop\cate\type  it jobs",
    r"C:\Users\krkc6\Desktop\clustered\it_jobs_test")


def intersection_words(unique_kws_file):
    list_jds = []
    jds = open(unique_kws_file, "r", encoding='utf-8').readlines()
    for jd in jds:
        jd = jd.lower().split()
        if len(jd)>0:
            list_jds.append(jd)
    return list_jds


list_jds = intersection_words(r"C:\Users\krkc6\Desktop\clustered\it_jobs_test")


#print(list_jds)
print(len(list_jds))


from functools import reduce

import numpy as np

# for i in range(len(list_jds)):
#     for j in range(i+2):

k = reduce(np.intersect1d, (list_jds[4:6]))
print(list(k))



