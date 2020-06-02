import re
import pandas as pd
import sys, os
import numpy as np
import nltk
from nltk import ngrams
import operator
import math


def parse_file(filename, n):
    f = open(filename, 'r')
    results = {}
    for line in f:
        words = clean_phrase(line).split(" ")
        grams = ngrams(words, n)
        for tup in grams:
            phrase = " ".join(tup)
            if phrase in results.keys():
                results[phrase] += 1
            else:
                results[phrase] = 1
    return results


def clean_phrase(line):
    return re.sub(r'[^\w\s]', '', line.replace('\n', '').replace('\t', '').lower())


def load_skills(filename):
    f = open(filename, 'r')
    skills = []
    for line in f:
        # removing punctuation and upper cases
        skills.append(clean_phrase(line))
    f.close()
    return list(set(skills))  # remove duplicates


def build_ngram_distribution(filename):
    n_s = [1, 2, 3]  # mono-, bi-, and tri-grams
    dist = {}
    for n in n_s:
        dist.update(parse_file(filename, n))
    return dist


softskills = load_skills('softskills.txt')
hardskills = load_skills('hardskills.txt')
jb_distribution = build_ngram_distribution("my_resume.txt")
cv_distribution = build_ngram_distribution("tesla_job_description.txt")
table = []
outFile = "Extracted_keywords.csv"


def measure1(v1, v2):
    return v1 - v2


def measure2(v1, v2):
    return max(v1 - v2, 0)


def measure3(v1, v2):  # cosine similarity
    # "compute cosine similarity of v1 to v2: (v1 dot v2)/{||v1||*||v2||)"
    sumxx, sumxy, sumyy = 0, 0, 0
    for i in range(len(v1)):
        x = v1[i]
        y = v2[i]
        sumxx += x * x
        sumyy += y * y
        sumxy += x * y
    return sumxy / math.sqrt(sumxx * sumyy)


def sendToFile(outFile, table):
    try:
        os.remove(outFile)
    except OSError:
        pass
    df = pd.DataFrame(table, columns=['type', 'skill', 'job', 'cv', 'm1', 'm2'])
    df_sorted = df.sort_values(by=['job', 'cv'], ascending=[False, False])
    df_sorted.to_csv(outFile, columns=['type', 'skill', 'job', 'cv'], index=False)
    print(df_sorted)


def printMeasures(table):
    n_rows = len(table)
    v1 = [table[m1][4] for m1 in range(n_rows)]
    v2 = [table[m2][5] for m2 in range(n_rows)]
    print("Measure 1: ", str(sum(v1)))
    print("Measure 2: ", str(sum(v2)))

    v1 = [table[jb][2] for jb in range(n_rows)]
    v2 = [table[cv][3] for cv in range(n_rows)]
    print("Measure 3 (cosine sim): ", str(measure3(v1, v2)))


def makeTable():
    # I am interested in verbs, nouns, adverbs, and adjectives
    parts_of_speech = ['CD', 'JJ', 'JJR', 'JJS', 'MD', 'NN', 'NNS', 'NNP', 'NNPS', 'RB', 'RBR', 'RBS', 'VB', 'VBD',
                       'VBG', 'VBN', 'VBP', 'VBZ']
    graylist = ["you", "will"]
    tmp_table = []
    # look if the skills are mentioned in the job description and then in your cv

    for skill in hardskills:
        if skill in jb_distribution:
            count_jb = jb_distribution[skill]
            if skill in cv_distribution:
                count_cv = cv_distribution[skill]
            else:
                count_cv = 0
            m1 = measure1(count_jb, count_cv)
            m2 = measure2(count_jb, count_cv)
            tmp_table.append(['hard', skill, count_jb, count_cv, m1, m2])

    for skill in softskills:
        if skill in jb_distribution:
            count_jb = jb_distribution[skill]
            if skill in cv_distribution:
                count_cv = cv_distribution[skill]
            else:
                count_cv = 0
            m1 = measure1(count_jb, count_cv)
            m2 = measure2(count_jb, count_cv)
            tmp_table.append(['soft', skill, count_jb, count_cv, m1, m2])

    # And now for the general language of the job description:
    # Sort the distribution by the words most used in the job description

    general_language = sorted(jb_distribution.items(), key=operator.itemgetter(1), reverse=True)
    for tuple in general_language:
        skill = tuple[0]
        if skill in hardskills or skill in softskills or skill in graylist:
            continue
        count_jb = tuple[1]
        tokens = skill.split()
        parts = nltk.pos_tag(tokens)
        if all([parts[i][1] in parts_of_speech for i in range(len(parts))]):
            if skill in cv_distribution:
                count_cv = cv_distribution[skill]
            else:
                count_cv = 0
            m1 = measure1(count_jb, count_cv)
            m2 = measure2(count_jb, count_cv)
            tmp_table.append(['general', skill, count_jb, count_cv, m1, m2])
    table = tmp_table
    return table


table = makeTable()
print(table)

send_to_file = sendToFile(outFile, table)
print(send_to_file)

cosine_similarity = printMeasures(table)
