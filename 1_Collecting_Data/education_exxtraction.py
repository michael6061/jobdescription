from __future__ import unicode_literals, print_function
from spacy.lang.en import English # updated




def extract_eduction(sample_jd):
    raw_text = sample_jd
    nlp = English()
    nlp.add_pipe(nlp.create_pipe('sentencizer'))  # updated
    doc = nlp(raw_text)
    sentences = [sent.string.strip() for sent in doc.sents]

    # print("sentences", sentences)

    # print(sentences)

    for sent in sentences:
        sent = sent.lower()
        if sent.__contains__("degree"):
            f = open("Eductations_extracted_degree.txt", "a")

            print("======eduction=======")
            print(sent)
            f.write(sent)
            f.write("\n")
            f.close()

# extract_eduction("education in this")
