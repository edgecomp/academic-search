from django.shortcuts import render, render_to_response
from .models import *
from stanfordcorenlp import StanfordCoreNLP
from nltk.corpus import stopwords
import json
import string
import time

nlp = StanfordCoreNLP(path_or_host='http://localhost', port=9000, timeout=50000)
nlp_props = {'annotators': 'tokenize, ssplit, lemma', 'piplineLanguage': 'en', 'outputFormat': 'json'}


# def search_operator_split(input):
#     if '&' in input:
#         return input.split('&')
#     elif '|' in input:
#         return input.split('|')
#     else:
#         return input

def append_keywords(ngram_keywords, new_keywords):
    for ngram_keyword in ngram_keywords:
        new_keywords.append(ngram_keyword)


def two_gram_search(new_keywords, ngram_keyword):
    twogram_objs = Keywords.objects.none()
    for i in range(len(new_keywords) - 1):
        multiple_word_keyword = new_keywords[i] + " " + new_keywords[i + 1]
        ngram_keyword.append(multiple_word_keyword)
        twogram_objs = twogram_objs | Keywords.objects.filter(keyword=multiple_word_keyword).order_by('-score')
    return twogram_objs


def three_gram_search(new_keywords, ngram_keyword):
    three_gram_objs = Keywords.objects.none()
    for i in range(len(new_keywords) - 2):
        multiple_word_keyword = new_keywords[i] + " " + new_keywords[i + 1] + " " + new_keywords[i + 2]
        ngram_keyword.append(multiple_word_keyword)
        three_gram_objs = three_gram_objs | Keywords.objects.filter(keyword=multiple_word_keyword).order_by('-score')
    return three_gram_objs


def four_gram_search(new_keywords, ngram_keyword):
    four_gram_objs = Keywords.objects.none()
    for i in range(len(new_keywords) - 3):
        multiple_word_keyword = new_keywords[i] + " " + new_keywords[i + 1] + " " + new_keywords[i + 2] + " " + new_keywords[i + 3]
        ngram_keyword.append(multiple_word_keyword)
        four_gram_objs = four_gram_objs | Keywords.objects.filter(keyword=multiple_word_keyword).order_by('-score')
    return four_gram_objs


def input_processing(keyword):
    annotated_string = nlp.annotate(keyword, properties=nlp_props)
    annotated_string = json.loads(annotated_string)
    tokens = annotated_string['sentences']
    stop_words = set(stopwords.words('english'))
    processed_keyword = list()
    for token_index in range(len(tokens)):
        sentence_prop = tokens[token_index]['tokens']
        for sentence_prop_index in range(len(sentence_prop)):
            word = sentence_prop[sentence_prop_index]['lemma']
            if not (word in string.punctuation or word in stop_words):
                processed_keyword.append(word)
        return processed_keyword


def home(request):
    return render(request, 'home.html')


def search(request):
    if 'search' in request.GET:
        input = request.GET['search']
        start = time.time()
        new_keywords = input_processing(input)
        objs = Keywords.objects.none()
        ngram_keyword = list()
        for keyword in new_keywords:
            objs = objs | Keywords.objects.filter(keyword=keyword).order_by('-score')
        if len(new_keywords) > 1:
            objs = objs | two_gram_search(new_keywords, ngram_keyword)
        if len(new_keywords) > 2:
            objs = objs | three_gram_search(new_keywords, ngram_keyword)
        if len(new_keywords) > 3:
            objs = objs | four_gram_search(new_keywords, ngram_keyword)
        conference_found = len(objs.values_list('conference_name').distinct())
        append_keywords(ngram_keyword, new_keywords)
        context = {
            'objects': objs,
            'keyword': new_keywords,
            'conference_found': conference_found
        }
    else:
        pass
    end = time.time()
    time_taken = end - start
    print(time_taken)
    return render_to_response('search_result.html', context)
