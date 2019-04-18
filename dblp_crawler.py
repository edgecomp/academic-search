from bs4 import BeautifulSoup
import requests
import pandas as pd
import os
import io
import re

DBLP_BASE_URL = 'http://dblp.uni-trier.de/'
PUB_SEARCH_URL = DBLP_BASE_URL + "search/publ/"
ARTICLES_DIR_PATH = ''


def set_articles_dir_path(path):
    global ARTICLES_DIR_PATH
    ARTICLES_DIR_PATH = path


def get_articles_dir_path():
    return ARTICLES_DIR_PATH


def create_data_files(directory):
    if not os.path.exists('db/'+directory):
        print('Creating directory '+directory)
        os.makedirs('db/'+directory)
    article_list = 'db/'+directory + '/articles.txt'
    if not os.path.isfile(article_list):
        write_file(article_list, '')


def write_file(path, data):
    f = open(path, 'w')
    f.write(data)
    f.close()


def append_to_existing_file(path, data):
    with io.open(path, 'a', encoding='utf-8') as fd:
        fd.write(data + '\n')


def build_query(search_string):
    request = requests.get(PUB_SEARCH_URL, params={'q': search_string})
    return BeautifulSoup(request.content, 'html.parser')


def scrape_data(pub):
    link = 'nothing'
    authors = []
    title = 'nothing'
    for li in pub:
        data = li.find("div", {"class": "data"})
        authors_a = data.findAll('span', attrs={"itemprop": "author"})
        for author in authors_a:
            authors.append(author.text)
        # print(authors)
        title = data.find('span', {"class": "title"}).text
        # print(title.text)
        publ = li.find("nav", {"class": "publ"})
        link_div = publ.find("div", {"class": "head"})
        link = link_div.find("a").get("href")
        # print(link)
    return {'Link': link,
            'Authors': authors,
            'Title': title}


def search_conference(search_string):

    soup = build_query(search_string)
    year = soup.find("li", {"class": "year"})
    pub = soup.findAll("li", {"class": "entry editor toc"})
    pub_list_data = []
    curr_year = 0

    # link = 'nothing'
    # authors = []
    # title = 'nothing'
    for li in pub:
        link = 'nothing'
        authors = []
        title = 'nothing'
        data = li.find("div", {"class": "data"})
        authors_a = data.findAll('span', attrs={"itemprop": "author"})
        for author in authors_a:
            authors.append(author.text)
        # print(authors)
        title = data.find('span', {"class": "title"}).text
        # print(title.text)
        publ = li.find("nav", {"class": "publ"})
        link_div = publ.find("div", {"class": "head"})
        link = link_div.find("a").get("href")
        pub_data = {'Link': link, 'Authors': authors, 'Title': title}
        pub_list_data.append(pub_data)

    return pd.DataFrame(pub_list_data)


def search_articles(conference_doc_url, directory_name):
    request = requests.get(conference_doc_url)
    soup = BeautifulSoup(request.content, 'html.parser')
    lis = soup.findAll('li', {"class": "entry inproceedings"})
    for li in lis:
        data = li.find("div", {"class": "data"})
        title = data.find('span', {"class": "title"}).text
        directory_name = re.sub(r'[^A-Za-z0-9|&]', r' ', directory_name).rstrip()
        create_data_files(directory_name)
        set_articles_dir_path('db/'+directory_name+'/articles.txt')
        append_to_existing_file(get_articles_dir_path(), title)

