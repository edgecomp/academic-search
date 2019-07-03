import pandas as pd
import json
import string
import re
import itertools
from nltk.corpus import stopwords
from multiprocessing import Queue
from multiprocessing.dummy import Pool as ThreadPool
from sklearn.feature_extraction.text import TfidfVectorizer


def threaded_work(function, documents, tfidf_vec, feature_names, conferences):
    q = Queue()
    pool = ThreadPool(8)
    pool.starmap(function, zip(documents, itertools.repeat(tfidf_vec), itertools.repeat(feature_names),
                               itertools.repeat(conferences), itertools.repeat(q)))
    pool.close()
    pool.join()
    columns = ['conferenceName', 'keyword', 'score']
    score_pd = pd.DataFrame(columns=columns)
    while not q.empty():
        score_pd = pd.concat([score_pd, q.get()], sort=False)
        score_pd = score_pd.reset_index(drop=True)
    q.close()
    return score_pd


def get_corpus(df, nlp, props):  # tokenize & lemmatize abstracts to processes a corpus
    conference_name = df['conference_type'].iloc[0]
    year = df['year'].iloc[0]
    abstracts = df['abstract']
    stop_words = set(stopwords.words('english'))
    lemmatized_corpus = ""
    for abstract in abstracts:
        abstract = abstract.lower()
        abstract = re.sub(r'[^A-Za-z0-9]', r' ', abstract)
        annotated_text = nlp.annotate(abstract, properties=props)
        annotated_text = json.loads(annotated_text)
        tokens = annotated_text['sentences']
        for token_index in range(len(tokens)):
            sentence_prop = tokens[token_index]['tokens']
            for sentence_prop_index in range(len(sentence_prop)):
                word = sentence_prop[sentence_prop_index]['lemma']
                if not (word in string.punctuation or word in stop_words):
                    lemmatized_corpus = lemmatized_corpus + word + " "
    return {'conference_name': conference_name + ' ' + str(year), 'corpus': lemmatized_corpus}


def get_individual_score(doc, tfidf_vec, feature_names, conferences, queue):  # get tf-idf score of each keyword
    feature_index = tfidf_vec[doc, :].nonzero()[1]
    tfidf_scores = zip(feature_index, [tfidf_vec[doc, x] for x in feature_index])
    keywords_with_score = []
    for keyword, score in [(feature_names[index], score) for (index, score) in tfidf_scores]:
        keywords_with_score.append({'conferenceName': conferences[doc], 'keyword': keyword, 'score': score})
    scores_pandas = pd.DataFrame.from_records(keywords_with_score)
    scores_pandas = scores_pandas.sort_values(by=['score'], ascending=False)
    top_50 = scores_pandas.head(50)
    queue.put(top_50)


def get_keywords_score(corpuses, conferences):
    vectorizer = TfidfVectorizer(ngram_range=(1, 4))
    tfidf_vec = vectorizer.fit_transform(corpuses)
    feature_names = vectorizer.get_feature_names()

    scores = threaded_work(get_individual_score, range(len(corpuses)), tfidf_vec, feature_names, conferences)
    return scores


def extract_keywords(conferences, corpuses):
    score_pd = get_keywords_score(corpuses, conferences)
    return score_pd
