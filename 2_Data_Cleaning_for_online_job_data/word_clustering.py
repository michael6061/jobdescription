from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import pandas as pd
import seaborn as sns
import re
from collections import defaultdict


def plot_wordcloud(text, mask=None, max_words=200000, max_font_size=100, figure_size=(10, 10),
                   title=None, title_size=20, image_color=False):
    stopwords = set(STOPWORDS)
    # define additional stop words that are not contained in the dictionary
    more_stopwords = {'one', 'br', 'Po', 'th', 'sayi', 'fo', 'Unknown', "you"}
    stopwords = stopwords.union(more_stopwords)
    # Generate the word cloud
    wordcloud = WordCloud(background_color='white',
                          stopwords=stopwords,
                          max_words=max_words,
                          max_font_size=max_font_size,
                          random_state=42,
                          width=800,
                          height=400,
                          mask=mask)
    wordcloud.generate(str(text))
    # set the plot parameters
    plt.figure(figsize=figure_size)
    if image_color:
        image_colors = ImageColorGenerator(mask);
        plt.imshow(wordcloud.recolor(color_func=image_colors), interpolation="bilinear");
        plt.title(title, fontdict={'size': title_size,
                                   'verticalalignment': 'bottom'})
    else:
        plt.imshow(wordcloud);
        plt.title(title, fontdict={'size': title_size, 'color': 'black',
                                   'verticalalignment': 'bottom'})
    plt.axis('off');
    plt.tight_layout()
    plt.show()

def ngram_extractor(text, n_gram):
    token = [token for token in text.lower().split(" ") if token != "" if token not in STOPWORDS]
    ngrams = zip(*[token[i:] for i in range(n_gram)])
    return [" ".join(ngram) for ngram in ngrams]


def generate_ngrams(df, n_gram, max_row):
    temp_dict = defaultdict(int)
    for question in df:
        for word in ngram_extractor(question, n_gram):
            temp_dict[word] += 1
    temp_df = pd.DataFrame(sorted(temp_dict.items(), key=lambda x: x[1])[::-1]).head(max_row)
    temp_df.columns = ["word", "wordcount"]
    return temp_df


def comparison_plot(df_1, df_2, col_1, col_2, space):
    fig, ax = plt.subplots(1, 2, figsize=(20, 10))

    sns.barplot(x=col_2, y=col_1, data=df_1, ax=ax[0], color="royalblue")
    sns.barplot(x=col_2, y=col_1, data=df_2, ax=ax[1], color="royalblue")

    ax[0].set_xlabel('Word count', size=14)
    ax[0].set_ylabel('Words', size=14)
    ax[0].set_title('Top 20 Bi-grams in Descriptions', size=18)

    ax[1].set_xlabel('Word count', size=14)
    ax[1].set_ylabel('Words', size=14)
    ax[1].set_title('Top 20 Tri-grams in Descriptions', size=18)

    fig.subplots_adjust(wspace=space)

    plt.show()

df = pd.read_csv("reed_uk.csv")

job_desc_na_cleaned = ""
for i, a in enumerate(df.iterrows()):
    print(a[1]["job_description"])
    jd = a[1]["job_description"]
    job_desc_na_cleaned = job_desc_na_cleaned + jd
    if i ==1000:
        break

print(job_desc_na_cleaned)


job_desc_na_cleaned = pd.DataFrame(np.array(job_desc_na_cleaned).reshape(-1))
job_cleaned = job_desc_na_cleaned.squeeze()

print(job_cleaned)
plot_wordcloud(job_cleaned, title="Word Cloud of job descriptions")
