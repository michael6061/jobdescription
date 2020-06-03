import pandas as pd
from collections import defaultdict

import re

def remove_filesIfolder():
    import os, shutil
    folder = r"C:\Users\krkc6\PycharmProjects\jobdescription\2_Data_Cleaning_for_online_job_data\jds_based_on_titles"

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

path_to_csv_file = r"C:\Users\krkc6\Desktop\reed_uk.csv"
df = pd.read_csv(path_to_csv_file)


kvmap= defaultdict(int)

job_desc = ""
for i, a in enumerate(df.iterrows()):
    jd = a[1]["job_description"]
    job_title = a[1]["job_title"]
    regex = re.compile('[^a-zA-Z0-9]')
    job_title_cleaned = regex.sub("", job_title )
    print(job_title_cleaned)
    kvmap[job_title] += 1
    # jds = open("C:\Users\krkc6\PycharmProjects\jobdescription\2_Data_Cleaning_for_online_job_data\jds_based_on_titles" + job_title_cleaned,
    #            "a", encoding='utf-8')
    # if job_title_cleaned == "ATMFieldServiceEngineerNorthWestLondon":
    with open("jds_based_on_titles/" + job_title_cleaned,  "a", encoding='utf-8') as jds:
        jds.write(str(jd))
        jds.write("\n")
    # jds.close()
    # if kvmap[a[1]["job_title"]]>10:
    #     print(kvmap[a[1]["job_title"]])

#
# # print(sort(kvmap))
# j = sorted(kvmap.items(), key=lambda x: x[1])
# print(j)

# for ele in j:
#     print(ele)







