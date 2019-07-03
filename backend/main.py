from conferenceFinder import *
from dblp_crawler import *
from scopus_scrapper import *
from multiprocessing.dummy import Pool as ThreadPool
from multiprocessing import Queue
from stanfordcorenlp import StanfordCoreNLP
from time import sleep
from db import *
from keywordExtractor import *
from similarConferenceFinder import *
import re
import pandas as pd
import datetime as dt
import itertools
import schedule
import numpy as np
import nltk

db = DB()
nlp = StanfordCoreNLP(path_or_host='http://localhost', port=9000, timeout=50000)
nlp_props = {'annotators': 'tokenize,ssplit,pos,lemma', 'pipelineLanguage': 'en', 'outputFormat': 'json'}


def set_conference_db(corpus_dict):
    db.insert_conference(corpus_dict)


def set_keywords_db(df):
    db.insert_allkeywords(df)


def remove_unwanted_charac(string_input):
    adjusted_string = re.sub("[\(\[].*?[\)\]]", "", string_input)
    adjusted_string = re.sub(r'[^A-Za-z0-9]', r' ', adjusted_string)  # for checkin article belongs to same conference
    return adjusted_string


def get_article_data(article, conference_name, year, apikey_index, queue):
    article_name = re.sub("[\(\[].*?[\)\]]", "", article) #remove brackets and string within
    article_name_query = re.sub(r'[^A-Za-z0-9|:|\-|\\|.|,|\']', r' ', article_name)# replace other unwanted character from query
    conference_name_keyword = remove_unwanted_charac(conference_name)
    try:
        single_arti_data_in_list = scopus_search("TITLE(" + article_name_query + ")",
                                conference_name_keyword, conference_name, year, apikey_index)
        if single_arti_data_in_list is None:
            pass
        else:
            queue.put(single_arti_data_in_list)  # shared resource, queue to store each data
            sleep(0.1)
    except Exception as excep:
        print('error: ', excep)
    finally:
        pass


def get_list_of_years():
    years = list()
    current_year = dt.datetime.now().year
    for year_diff in range(8):
        years.append(current_year - year_diff)
    return years


def threaded_work(article_list, conference_type, year, apikey_index):
    try:
        q = Queue()
        pool = ThreadPool(6)
        pool.starmap(get_article_data, zip(article_list, itertools.repeat(conference_type),
                                           itertools.repeat(year), itertools.repeat(apikey_index), itertools.repeat(q)))
        pool.close()
        pool.join()
        metadata = []
        while not q.empty():
            metadata.append(q.get())
        q.close()
        return metadata
    except Exception as excep:
        print(excep)
    finally:
        pass


def set_keywords():
    conferences_data = db.get_all_data_from_table('conferences_temp')
    corpuses = []
    conferences = []
    for row in conferences_data:
        conferencename = row[0]
        db.update_metadata(conferencename)  # place corresponding conference name(foreign key)
        conferences.append(conferencename)
        corpuses.append(row[1])
    set_keywords_db(extract_keywords(conferences, corpuses))  # extracts keywords & tfidf scores from each corpus


def set_similar_confs():
    keywords_df = create_collaborative_keyworddb(db)
    neighbor_conf_data = get_neigbors(keywords_df)
    for row in neighbor_conf_data.itertuples(index=False):
        neighbor_conf_name = row[1]
        conferencename = row[0]
        db.update_conferencestemp_table(neighbor_conf_name, conferencename)


def clear_temp_db():
    db.truncate_table('metadata_temp')  # clear table
    db.truncate_table('keywords_temp')
    db.truncate_table('conferences_temp')


def update_main_db():
    db.truncate_table('conferences')  # clear table
    db.copy_data_to_another_table('conferences', 'conferences_temp') #copy temp table to normal table
    db.truncate_table('metadata')
    db.copy_data_to_another_table('metadata', 'metadata_temp')
    db.truncate_table('keywords')
    db.copy_data_to_another_table('keywords', 'keywords_temp')


def main():
    conferencelist = get_conference_names()
    years = get_list_of_years()
    apikey_index = 0
    clear_temp_db()
    for year in years:
        for conference_type in conferencelist:
            conference_searched_result = scrape_conference([conference_type + ' year:' + str(year) + ':'])
            if not conference_searched_result.empty:
                conference_url = str(conference_searched_result.iloc[0][1])
                article_list = scrape_articles(conference_url)
                metadata = threaded_work(article_list, conference_type, year, apikey_index)
                if bool(metadata) is False:
                    pass
                else:
                    metadata_df = pd.DataFrame(metadata)
                    db.insert_allmetadata(metadata_df)
                    global nlp, nlp_props
                    corpus = get_corpus(metadata_df, nlp, nlp_props)
                    set_conference_db(corpus)
            else:
                pass
        apikey_index = apikey_index + 1  # for each year on scopus api key
    set_keywords()
    set_similar_confs()
    update_main_db()


if __name__ == '__main__':
    # nltk.download('stopwords') # download to get stopwords only need to perform once
    schedule.every().saturday.at("08:10").do(main)
    while True:
        schedule.run_pending()
