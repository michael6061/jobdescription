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