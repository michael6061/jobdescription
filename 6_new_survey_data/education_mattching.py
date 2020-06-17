import pandas as pd
import csv
import re
from collections import defaultdict
import requests
import xlwt
import os
from bs4 import BeautifulSoup

matched = "yes"

path_to_clean_files = r"scraped_data"
def remove_files_in_folder():
    import os, shutil
    folder = path_to_clean_files
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


def scraping_web(job_title):
    # remove_files_in_folder()
    BASE_URL = "https://www.reed.co.uk/"
    def preprocess(text):
        modified_text = ''
        for letter in text:
            if letter == ' ':
                letter = '-'
            modified_text += letter.lower()

        return modified_text

    def job_url(key, num):
        modified_key = preprocess(key)
        return BASE_URL + 'jobs/' + modified_key + '-jobs?' + 'pageno=' + str(num)

    def job_detail_url(key, title, id):
        modified_title = preprocess(title)
        modified_key = preprocess(key)
        return BASE_URL + 'jobs/' + modified_title + '/' + str(
            id) + '?source=searchResults#/jobs/' + modified_key + '-jobs'


    keywords = job_title

    BASE_URL = "https://www.reed.co.uk/"

    count = 0
    # for i in range(1):
    key = job_title
    key = key.lower()
    jd_list = []
    jd_text_list = []
    title_list = []

    for num in range(1):
        url = job_url(key, num)
        response = requests.get(url)

        soup = BeautifulSoup(response.content, "html.parser")

        # articles = soup.select('article', {'class': 'job-result'})
        articles = soup.select('article')

        for article_count, job in enumerate(articles):
            count +=1


            title = job.find('h3').get_text()[1:-1].lower()
            id = job.get('id')[10:]

            if title[-1] == ' ':
                title = title[:-1]
            detail_url = job_detail_url(key, title, id)
            # print(detail_url)

            response2 = requests.get(detail_url)
            print("detail_url : ", article_count, detail_url)
            soup2 = BeautifulSoup(response2.content, "html.parser")
            skills = soup2.select('div.skills  ul li')
            jd = soup2.select('div.description  span')
            jd_list.append(jd)
            try:
                jd_text_list.append(jd[0].text)
                title_list.append(title)
            except:
                pass

        return jd_list, jd_text_list, title_list


            # summary = pd.DataFrame({ 'Cosine Distances': detail_url, 'Job Description': jd})
            # summary.to_csv(r"scraped_data/data_collected.csv", mode='a',header=False, index=False, encoding="utf-8")



            # if len(jd) > 0:
            #     try:
            #         # print(jd[0].text)
            #         jd_text = jd[0].text
            #         # extract_eduction(jd_text)
            #     except:
            #         print("failed_extract_edu")

def mapping(jd):
    arr = list(map(str, jd.strip().split()))
    result = ["No degree or GCSE"]
    for i in range(len(arr)):
        if arr[i].__contains__("degree") or arr[i].__contains__("Degree")  or arr[i].__contains__("GCSE") :
            result = arr[i - 5:i + 5]
            return result
    return result


directory = r"matched_education_files"
path_to_csv_file = r"lf_survey_v1.csv"
df = pd.read_csv(path_to_csv_file)
count_nan = 0
count_exist = 0
job_titles = []
educations = []


def query_reed(job_title):
    regex = re.compile('[^a-zA-Z0-9 ]')
    job_title_cleaned = regex.sub("", str(job_title))
    jd_list, jd_text , title_list= scraping_web(job_title_cleaned)

    # f_lines = open(r"scraped_data/data_collected.csv", "r", encoding="UTF-8").readlines()
    # print(f_lines)
    for jd,online_title in zip(jd_text, title_list):
        print(jd)
        with open(r"matched_education_files/" + job_title_cleaned, mode='a', encoding='utf-8') as employee_file:
            employee_file.write(job_title_cleaned)
            employee_file.write(" | ")
            employee_file.write(online_title)
            employee_file.write(" | ")
            employee_file.write(str(mapping(jd)))
            employee_file.write("\n")



# job_eductation =
for i, a in enumerate(df.iterrows()):
    education = str(a[1]["HIQUL15D"])
    job_title = a[1]["SC102KM"]
    if pd.notna(job_title) == True :
        count_exist+=1
        job_titles.append(job_title)
        educations.append(education)
    else:
        count_nan +=1


unique_job_list = list(set(job_titles))  #It removes duplicates, and gives unique job titles
unique_education_list = list(set(educations))
print(len(unique_job_list))
print(len(unique_education_list))

print(unique_education_list)
for unique_job_title in unique_job_list:
    print(unique_job_title)
    try:
        pass
        # query_reed(unique_job_title)
    except:
        print("Exception : " , unique_job_title)



edu_categories = ['Higher education', 'GCSE grades A*-C or equivalent', 'Degree or equivalent', 'GCE A level or equivalent']

def education_string_match(line, job_title):
    line  = line.lower()
    if line.__contains__('no degree or gcse'):
        return 0, "None"
    if line.__contains__("degree"):
        return 1, 'Degree or equivalent'
    if line.__contains__("gcse"):
        return 1, 'GCSE grades A*-C or equivalent'


#         return 1, 'Degree or equivalent'    # if line.__contains__('no degree or gcse'):
    #     pass
    # elif line.__contains__("gcse") or line.__contains__("degree"):
    #     # print(line)
    #     if  line.__contains__("degree") :
    #         return 1, 'Degree or equivalent'
    #     if line.__contains__("gcse"):
    #         return 1, 'GCSE grades A*-C or equivalent'
    #     if line.__contains__("high"):
    #         return 1, 'Higher education'
    # else:
    #     return 0, "None"


# edu_categories = ['No qualification', 'nan', 'Other qualification', 'Higher education', "Don't know", 'GCSE grades A*-C or equivalent', 'Degree or equivalent', 'GCE A level or equivalent']
def education_output(job_title_cleaned):
    try:
        if pd.notna(job_title) == True :
            with open(r"matched_education_files/" + job_title_cleaned, mode='r', encoding='utf-8') as job_title_education:
                for line in job_title_education:
                    dig, edu = education_string_match(line, job_title)
                    if dig ==1:
                        return edu
    except:
        pass
    return "Other qualification"


f = open("education_comparision.csv", "w")
f.write("Job Title")
f.write( " | ")
f.write( "Survey")
f.write(" | ")
f.write( "Online")
f.write("\n")


exact_match_count = 0
survey_data = [0]*5
online_data = [0]*5
edu_classes = ['Higher education', 'GCSE grades A*-C or equivalent', 'Degree or equivalent', 'GCE A level or equivalent', 'Other qualification']



test_list = []
for i, a in enumerate(df.iterrows()):
    education = str(a[1]["HIQUL15D"])
    job_title = a[1]["SC102KM"]
    if pd.notna(job_title) == False :
        print("NAN JOBTITLE")
    else:
        regex = re.compile('[^a-zA-Z0-9 ]')
        job_title_cleaned = regex.sub("", str(job_title))
        edu_result_tag = education_output(job_title_cleaned)
        if education in edu_classes:
            indx = edu_classes.index(education)
            survey_data[indx] = survey_data[indx] + 1
        if education not in edu_categories:
            education = "Other qualification"
        if education == edu_result_tag:
            test_list.append(edu_result_tag)
            exact_match_count +=1


        if edu_result_tag in edu_classes:
            o_indx = edu_classes.index(edu_result_tag)
            online_data[o_indx] = online_data[o_indx] + 1
        f.write(job_title_cleaned)
        f.write(" | ")
        f.write(education)
        f.write(" | ")
        f.write(edu_result_tag)
        f.write("\n")

f.close()

print("exact_match_count", exact_match_count)
print("job nan", count_nan)
print("job exist", count_exist)
print("survey_data", survey_data)
print("online_data", online_data)
# print("test_list", test_list)



# import matplotlib.pyplot as plt
# import numpy as np
# N = len([1])
# survey_data = (exact_match_count)
# online_data= (count_exist - exact_match_count )
# ind = np.arange(N)
# plt.figure(figsize=(5,5))
# width = 0.3
# plt.bar(ind, survey_data , width, label='Exact Match')
# plt.bar(ind + width, online_data, width, label='Not match')
# plt.ylabel('Here goes y-axis label')
# plt.title('Edu match vs not match')
# plt.xticks(ind + width / 2, edu_classes)
# plt.legend(loc='best')
# plt.show()


def plot_five_categories():
    edu_classes = ['Higher education', 'GCSE grades A*-C or equivalent', 'Degree or equivalent', 'GCE A level or equivalent', 'Other qualification']

    import matplotlib.pyplot as plt
    import numpy as np
    N = len(edu_classes)
    # survey_data = survey_data
    # online_data= online_data
    ind = np.arange(N)
    plt.figure(figsize=(16,5))
    width = 0.3
    plt.bar(ind, survey_data , width, label='Survey Data')
    plt.bar(ind + width, online_data, width, label='Online Data')
    plt.ylabel('Number of jobs')
    plt.title('Categoriees of jobs')
    plt.xticks(ind + width / 2, edu_classes)
    plt.legend(loc='best')
    plt.show()

plot_five_categories()