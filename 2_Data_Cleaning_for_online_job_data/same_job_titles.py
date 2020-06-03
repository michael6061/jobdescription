import pandas as pd
from collections import defaultdict

import re

df = pd.read_csv("reed_uk.csv")

print(df)

kvmap= defaultdict(int)

job_desc = ""
for i, a in enumerate(df.iterrows()):
    # print(a[1]["job_title"])
    jd = a[1]["job_description"]
    # job_desc = job_desc + jd
    job_title = a[1]["job_title"]
    # job_title_cleaned = job_title.replace("/" , "_").replace(" ", "_")
    regex = re.compile('[^a-zA-Z]')
    job_title_cleaned = regex.sub("_", job_title )


    print(job_title_cleaned)
    kvmap[job_title] += 1
    if job_title_cleaned == "Assistant_General_Manager":
        with open("jds_based_on_titles/" + job_title_cleaned, "a") as jds:
            jds.write(str(jd.split(" ")))
            jds.write("\n")
    # if kvmap[a[1]["job_title"]]>10:
    #     print(kvmap[a[1]["job_title"]])
    if i ==100:
        break
#
# # print(sort(kvmap))
# j = sorted(kvmap.items(), key=lambda x: x[1])
# print(j)

# for ele in j:
#     print(ele)







