import pandas as pd
import csv
import re
from collections import defaultdict
import requests
import xlwt
from bs4 import BeautifulSoup
matched = "yes"
path_to_clean_files = r"C:\Users\krkc6\PycharmProjects\jobdescription\6_new_survey_data\scraped_data"
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
    remove_files_in_folder()
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

    # keywords = ["Administration", "Retail", "Sales & Marketing",
    #             "Accountant", "Social Care"]

    keywords = job_title

    BASE_URL = "https://www.reed.co.uk/"

    count = 0
    for i in range(5):
        key = keywords[i]
        key = key.lower()

        for num in range(1, 31):
            url = job_url(key, num)
            response = requests.get(url)
            print(url)

            soup = BeautifulSoup(response.content, "html.parser")

            # articles = soup.select('article', {'class': 'job-result'})
            articles = soup.select('article')

            for job in articles:
                count +=1
                print(count)

                title = job.find('h3').get_text()[1:-1].lower()
                id = job.get('id')[10:]

                if title[-1] == ' ':
                    title = title[:-1]
                detail_url = job_detail_url(key, title, id)
                # print(detail_url)

                response2 = requests.get(detail_url)
                soup2 = BeautifulSoup(response2.content, "html.parser")
                skills = soup2.select('div.skills  ul li')
                jd = soup2.select('div.description  span')
                print(jd)
                if count > 20:
                    print("here")
                    return
                summary = pd.DataFrame({
                    # 'Company': companies,
                    # 'Postition': positions,
                    'Cosine Distances': detail_url,
                    # 'Keywords': key_list,
                    'Job Description': jd
                })
                summary.to_csv(
                    r"C:\Users\krkc6\PycharmProjects\jobdescription\6_new_survey_data\scraped_data\data_collected.csv", mode='a',
                    header=False, index=False, encoding="utf-8")

                # with open(r"jds_csv_files/data.csv", mode='w', encoding='utf-8') as employee_file:
                #     employee_file.write(str(jd))
                #     employee_file.write("\n")

                if len(jd) > 0:
                    try:
                        # print(jd[0].text)
                        jd_text = jd[0].text
                        # extract_eduction(jd_text)
                    except:
                        print("failed_extract_edu")

def mapping(jd):
    global matched
    arr = list(map(str, jd.strip().split()))
    result = ["No degree or GCSE"]
    global count
    for i in range(len(arr)):
            # print(arr[i])
        if arr[i].__contains__("degree") or arr[i].__contains__("GCSE"):


            result = arr[i - 5:i + 5]
            return result
    matched = "no"
    return result



path_to_csv_file = r"C:\Users\krkc6\Desktop\Survey Data.csv"
df = pd.read_csv(path_to_csv_file)
for i, a in enumerate(df.iterrows()):
    education = str(a[1]["edumode_new"])
    job_title = a[1]["jbisco88_cc"]
    salary = str(a[1]["income_r"])
    regex = re.compile('[^a-zA-Z0-9]')
    job_title_cleaned = regex.sub("", str(job_title))
    scraping_web(job_title_cleaned)
    f = open(r"C:\Users\krkc6\PycharmProjects\jobdescription\6_new_survey_data\scraped_data\data_collected.csv", "r",encoding="UTF-8").readlines()
    for line in f:
        line = line.strip().replace("\n", "")
        print(line)
        print("in writing part")
        degree_specification = mapping(line)
        with open(r"C:\Users\krkc6\PycharmProjects\jobdescription\6_new_survey_data\matched_education_files/" + job_title_cleaned, mode='a',encoding='utf-8') as employee_file:
            employee_file.write(job_title_cleaned)
            employee_file.write(" | ")
            employee_file.write(education)
            employee_file.write(" | ")
            employee_file.write(salary)
            employee_file.write(" | ")
            employee_file.write("qualification match  " + matched)
            employee_file.write(" | ")
            employee_file.write(str(degree_specification))
            employee_file.write("\n")