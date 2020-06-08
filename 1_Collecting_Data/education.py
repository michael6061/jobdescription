import pandas as pd
import csv
from collections import defaultdict
count = 0
import re
#t =  str(input("enter categeory"))
path_to_cleaned_files = r"C:\Users\krkc6\PycharmProjects\jobdescription\1_Collecting_Data\jds_qualification_per_job"
path2 = r"C:\Users\krkc6\PycharmProjects\jobdescription\1_Collecting_Data\jds_csv_files"
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

def remove_files_in_folder2():
    import os, shutil
    folder = path2
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

remove_files_in_folder2()

def mapping(jd):
    arr = list(map(str, jd.strip().split()))
    result = ["No match"]
    global count
    for i in range(len(arr)):
        #print(arr[i])
        if arr[i].__contains__("degree") or arr[i].__contains__("qualification"):
            lis = [arr[i-5:i+5]]
            # for j in lis:
            #     if j.__contains__("engineering") or j.__contains__("bachelor"):
            #         print(j)
            #     elif j.__contains__("science") or j.__contains__("mechanical"):
            #         print(j)


            result =  arr[i - 5:i + 5]
            return result
    count = 1+count
    #print(count)
    return result






path_to_csv_file = r"C:\Users\krkc6\Desktop\reed_uk.csv"
df = pd.read_csv(path_to_csv_file)
for i, a in enumerate(df.iterrows()):
    jd = a[1]["job_description"]
    job_title = a[1]["job_title"]
    regex = re.compile('[^a-zA-Z0-9]')
    job_title_cleaned = regex.sub("", job_title)
    degree_specification = mapping(jd)
    # if t == job_title_cleaned:
    #     print(degree_specification)
    with open(r"jds_csv_files/education1.csv", mode='a', encoding='utf-8') as employee_file:
        employee_file.write(job_title_cleaned)
        employee_file.write(" | ")
        employee_file.write(jd)
        employee_file.write(" | ")
        employee_file.write(str(degree_specification))
        employee_file.write("\n")


    #print(str(degree_specification))
    if degree_specification != "None":
        with open("jds_qualification_per_job/" + job_title_cleaned, "a", encoding='utf-8') as ff:
            ff.write(str(degree_specification) + "\n")
            ff.write("\n")



