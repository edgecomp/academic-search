from django.shortcuts import render, render_to_response
from .models import *
from stanfordcorenlp import StanfordCoreNLP
from nltk.corpus import stopwords
import json
import string
import time

nlp = StanfordCoreNLP(path_or_host='http://localhost', port=9000, timeout=50000)
nlp_props = {'annotators': 'tokenize, ssplit, lemma', 'piplineLanguage': 'en', 'outputFormat': 'json'}


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
        new_keywords = input_processing(input)
        singlegramobjs = Keywords.objects.none()
        bigramobjs = Keywords.objects.none()
        trigramobjs = Keywords.objects.none()
        quadgramobjs = Keywords.objects.none()
        allkeywords = list()
        bigram_keyword = list()
        trigram_keyword = list()
        quadgram_keyword = list()
        singlegram_keyword = new_keywords
        print(singlegram_keyword)
        for keyword in new_keywords:
            singlegramobjs = singlegramobjs | Keywords.objects.filter(keyword=keyword).order_by('-score')
        if len(new_keywords) > 1:
            bigramobjs = bigramobjs | two_gram_search(new_keywords, bigram_keyword)
        if len(new_keywords) > 2:
            trigramobjs = trigramobjs | three_gram_search(new_keywords, trigram_keyword)
        if len(new_keywords) > 3:
            quadgramobjs = quadgramobjs | four_gram_search(new_keywords, quadgram_keyword)
        append_keywords(singlegram_keyword, allkeywords)
        append_keywords(bigram_keyword, allkeywords)
        append_keywords(trigram_keyword, allkeywords)
        append_keywords(quadgram_keyword, allkeywords)
        context = {
            'singlegramobjs': singlegramobjs,
            'bigramobjs': bigramobjs,
            'trigramobjs': trigramobjs,
            'quadgramobjs': quadgramobjs,
            'allkeywords': allkeywords,
            'singlegramkeywords': singlegram_keyword,
            'bigramkeywords': bigram_keyword,
            'trigramkeywords': trigram_keyword,
            'quadgramkeywords': quadgram_keyword
        }
    else:
        pass
    return render_to_response('search_result.html', context)
