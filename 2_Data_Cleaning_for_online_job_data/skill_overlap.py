import nltk
import pandas as pd
import re
from nltk.tokenize import word_tokenize
import io
from nltk.corpus import stopwords

stop_words = set(stopwords.words('english'))
path_to_jds_based_title_file = r"C:\Users\krkc6\PycharmProjects\jobdescription\2_Data_Cleaning_for_online_job_data\jds_based_on_titles\Analyst"
path_to_cleaned_files = r"C:\Users\krkc6\PycharmProjects\jobdescription\2_Data_Cleaning_for_online_job_data\jobs_per_line_unique_words"
path_to_individual_clened_files = r"C:\Users\krkc6\PycharmProjects\jobdescription\2_Data_Cleaning_for_online_job_data\jobs_per_line_unique_words\Analyst_test"

def remove_files_in_folder():
    import os, shutil
    folder = path_to_cleaned_files
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

remove_files_in_folder()

def jdfile_to_kws_file(jdfile_path, jd_kw_file):
    jdfile = open(jdfile_path)

    lines = jdfile.readlines()
    print(lines)
    appendFile = open(jd_kw_file, 'a')
    print(type(lines))

    for line in lines:
        words = line.split(" ")
        for r in words:
            if not r in stop_words:
                appendFile.write(" " + r)

        appendFile.write("\n")
    appendFile.close()


jdfile_to_kws_file(path_to_jds_based_title_file,path_to_individual_clened_files)

def intersection_list(unique_kws_file):
    list_jds = []
    jds = open(unique_kws_file).readlines()
    for jd in jds:
        jd = jd.lower().split()
        if len(jd)>0:
            list_jds.append(jd)
    return list_jds

list_jds = intersection_list(path_to_individual_clened_files)

print(list_jds)
print(len(list_jds))
from functools import reduce
import numpy as np

def intersection_words(list_jds):
    for i in range(len(list_jds)):
        for j in range(len(list_jds)):
            print(i,j)
            k = (np.intersect1d, ([list_jds[i] , list_jds[j]]))
            print(list(k))
intersection_words(list_jds)
