import requests
import xlwt
from bs4 import BeautifulSoup
# from custom_functions import job_url, job_detail_url

from education_exxtraction import extract_eduction

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
    return BASE_URL + 'jobs/' + modified_title + '/' + str(id) + '?source=searchResults#/jobs/' + modified_key + '-jobs'


keywords = ["Administration", "Retail", "Sales & Marketing",
            "Accountant", "Social Care"]

BASE_URL = "https://www.reed.co.uk/"

for i in range(5):
    key = keywords[i]
    key = key.lower()

    for num in range(1, 31):
        url = job_url(key, num)
        response = requests.get(url)
        print(response)

        soup = BeautifulSoup(response.content, "html.parser")

        # articles = soup.select('article', {'class': 'job-result'})
        articles = soup.select('article')

        for job in articles:
            title = job.find('h3').get_text()[1:-1].lower()
            id = job.get('id')[10:]

            if title[-1] == ' ':
                title = title[:-1]
            detail_url = job_detail_url(key, title, id)

            response2 = requests.get(detail_url)
            soup2 = BeautifulSoup(response2.content, "html.parser")
            skills = soup2.select('div.skills  ul li')
            jd = soup2.select('div.description  span')

            if len(jd) > 0:
                try:
                    # print(jd[0].text)
                    jd_text = jd[0].text
                    extract_eduction(jd_text)
                except:
                    print("failed_extract_edu")
