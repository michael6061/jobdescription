import matplotlib.pyplot as plt
import numpy as np
f = open("New_csv_with_edu_match.csv", "r")
import pandas
import matplotlib.pyplot as plt
import numpy as np

import pandas as pd
df = pd.read_csv("New_csv_with_edu_match.csv" , delimiter="\ \|\ ")



def plot_male_female(df):
    total_male = 0
    total_female = 0

    male_match = 0
    male_unmatch = 0
    female_match = 0
    female_unmatch = 0

    for i, a in enumerate(df.iterrows()):
        # print(a[1][" age "])
        # print(a[1][" sex "])

        if a[1]["sex"] == "Male":
            total_male +=1
            if a[1]["Edu Match"]==1:
                male_match +=1
            else:
                male_unmatch += 1

        if a[1]["sex"] == "Female":
            total_female += 1
            if a[1]["Edu Match"]==1:
                female_match +=1
            else:
                female_unmatch += 1

    print("Total Male : ", total_male )
    print("Total Female : ", total_female )
    print("Total Male Match: ",male_match)
    print("Total Male Unmatch: ",male_unmatch)
    print("Total Female Match : ",female_match)
    print("Total Female unmatch : ",female_unmatch)

    df = pandas.DataFrame(dict(graph=['Male', 'Female'],
                               n=[male_match, female_match], m=[male_unmatch, female_unmatch]))

    ind = np.arange(len(df))
    width = 0.4

    fig, ax = plt.subplots()
    ax.barh(ind + width, df.m, width, color='blue', label='Unmatch')
    ax.barh(ind, df.n, width, color='orange', label='Match')


    ax.set(yticks=ind + width, yticklabels=df.graph, ylim=[2*width - 1, len(df)])
    ax.legend()
    plt.xlabel('Number of jobs')
    plt.title('Sex based Education mismatch')

    plt.show()

# plot_male_female(df)
def plot_five_categories(df):
    edu_classes = ['Higher education', 'GCSE grades A*-C or equivalent', 'Degree or equivalent', 'GCE A level or equivalent', 'Other qualification']
    survey_data = [0] * 5
    online_unmatch_data = [0] * 5
    online_match_data = [0] * 5
    for i, a in enumerate(df.iterrows()):
        education = str(a[1]["Education"])
        if education in edu_classes:
            indx = edu_classes.index(education)
            survey_data[indx] = survey_data[indx] + 1
        edu_result_tag = str(a[1]["Edu Match"])
        # print(edu_result_tag)

        if edu_result_tag=="1":
            # o_indx = edu_classes.index(edu_result_tag)
            online_match_data[indx] = online_match_data[indx] + 1


    print(survey_data)
    online_unmatch_data = [0]*5
    for i, ele in enumerate(online_unmatch_data):
        online_unmatch_data[i] = survey_data[i] - online_match_data[i]
    print(online_match_data)

    N = len(edu_classes)
    ind = np.arange(N)
    plt.figure(figsize=(16,5))
    width = 0.3
    plt.bar(ind, online_unmatch_data , width, label='Mismatch')
    plt.bar(ind + width, online_match_data, width, label='Edu Match')
    plt.ylabel('Number of jobs')
    plt.title('Categoriees of jobs')
    plt.xticks(ind + width / 2, edu_classes)
    plt.legend(loc='best')
    plt.show()

# plot_five_categories(df)




import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import six


def render_mpl_table(data, col_width=3.0, row_height=0.625, font_size=14,
                     header_color='#40466e', row_colors=['#f1f1f2', 'w'], edge_color='w',
                     bbox=[0, 0, 1, 1], header_columns=0,
                     ax=None, **kwargs):
    if ax is None:
        size = (np.array(data.shape[::-1]) + np.array([0, 1])) * np.array([col_width, row_height])
        fig, ax = plt.subplots(figsize=size)
        ax.axis('off')

    mpl_table = ax.table(cellText=data.values, bbox=bbox, colLabels=data.columns, **kwargs)

    mpl_table.auto_set_font_size(False)
    mpl_table.set_fontsize(font_size)

    for k, cell in  six.iteritems(mpl_table._cells):
        cell.set_edgecolor(edge_color)
        if k[0] == 0 or k[1] < header_columns:
            cell.set_text_props(weight='bold', color='w')
            cell.set_facecolor(header_color)
        else:
            cell.set_facecolor(row_colors[k[0]%len(row_colors) ])
    ax.get_figure()
    plt.show()
    return ax



# render_mpl_table(df, header_columns=0, col_width=2.0)

from collections import Counter

def job_title_count_match_mismatch():
    jts = []
    df_table = pd.DataFrame()
    df_jt = []
    df_match = [0]*10
    df_unmatch = [0]*10

    for i, a in enumerate(df.iterrows()):
        jt = str(a[1]["Job Title"])
        jts.append(jt)
    dic = Counter(jts)
    print(dic)
    print(dic.most_common(10))
    for jt in dic.most_common(10):
        df_jt.append(jt[0])
    print("df_jt", df_jt)

    for i, a in enumerate(df.iterrows()):
        jt = str(a[1]["Job Title"])
        edu_result_tag = str(a[1]["Edu Match"])
        if jt in df_jt:
            indx = df_jt.index(jt)

            if edu_result_tag=="1":
                df_match[indx] = df_match[indx] +1
            else:
                df_unmatch[indx] = df_unmatch[indx] + 1

    df_table['job title'] = df_jt
    df_table['match'] = df_match
    df_table['unmatch'] = df_unmatch
    return df_table





# df_table = job_title_count_match_mismatch()


# render_mpl_table(df_table, header_columns=0, col_width=2.0)

def plot_bar_graph_from_list(l, title):
    import matplotlib.pyplot as plt;
    plt.rcdefaults()
    import numpy as np
    import matplotlib.pyplot as plt

    objects = [  (str(ele*10) + "-"+ str(ele*10 +9))     for ele in range(10)]
    y_pos = np.arange(len(objects))
    performance = l

    plt.bar(y_pos, performance, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    plt.ylabel('Number of candidates')
    plt.title(title)

    plt.show()


def age_edumatch_graphs(df):
    age_list_match = [0]*10
    age_list_unmatch = [0]*10

    for i, a in enumerate(df.iterrows()):
        # print(a[1][" age "])
        # print(a[1][" sex "])
        if (a[1]["age"]) == "99 and over":
            nums = [99]
        else:
            nums = [int(a[1]["age"])]
        for k, g in itertools.groupby(nums, key=lambda n: n // 10):
            print(k)
        if a[1]["Edu Match"] == 1:
            age_list_match[k] = age_list_match[k] +1
        else:
            age_list_unmatch[k] = age_list_unmatch[k] +1

    print(age_list_match)
    print(age_list_unmatch)
    plot_bar_graph_from_list(age_list_match, 'Edu match by age')
    plot_bar_graph_from_list(age_list_unmatch, 'Edu mismatch by age')



import itertools
nums = [1]
for k, g in itertools.groupby(nums, key=lambda n: n//10):
    print (k)

age_edumatch_graphs(df)

