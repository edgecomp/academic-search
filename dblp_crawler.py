from builtins import print
from bs4 import BeautifulSoup
import requests
import pandas as pd
import os
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
    with open(path, 'a', encoding='utf-8') as fd:
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
    # if 'year' in pub.get('class'):
    #     # year is not always scrapable, except for this case. Might be done more elegantly
    #     return int(pub.contents[0])
    # else:
    # ###############################original dblp code###############################################
    #     for content_item in pub.contents:
    #         class_of_content_item = content_item.attrs.get('class', [0])
    #
    #         if 'data' in class_of_content_item:
    #             for author in content_item.findAll('span', attrs={"itemprop": "author"}):
    #                 authors.append(author.text)
    #             title = content_item.find('span', attrs={"class": "title"}).text
    #         elif 'publ' in class_of_content_item:
    #             link = content_item.contents[0].find('a').attrs.get('href', "nothing")
    # ###############################################################################################
    return {'Link': link,
            'Authors': authors,
            'Title': title}


def search_conference(search_string):

    soup = build_query(search_string)
    year = soup.find("li", {"class": "year"})
    pub = soup.findAll("li", {"class": "entry editor toc"})

    # pub_list_raw = soup.find("ul", {"class": "publ-list"})
    # print(pub_list_raw.children)
    # pub_list_raw = pub_list_raw.findAll('li', {"class": "entry editor toc marked"})
    pub_list_data = []
    curr_year = 0

    # link = 'nothing'
    authors = []
    # title = 'nothing'
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
        pub_data = {'Link': link, 'Authors': authors, 'Title': title}
        pub_list_data.append(pub_data)
        link = 'nothing'
        authors = []
        title = 'nothing'
    # pub_data = scrape_data(pub)

    # # for child in pub_list_raw.children:
    #     pub_data = scrape_data(child)
    #     # print(pub_data)
    #     if type(pub_data) == int:
    #         curr_year = pub_data
    #     else:
    #         pub_data['Year'] = curr_year
    #         pub_list_data.append(pub_data)
    return pd.DataFrame(pub_list_data)


def search_articles(conference_doc_url, directory_name):
    request = requests.get(conference_doc_url)
    soup = BeautifulSoup(request.content, 'html.parser')
    lis = soup.findAll('li', {"class": "entry inproceedings"})
    for li in lis:
        data = li.find("div", {"class": "data"})
        title = data.find('span', {"class": "title"}).text
        directory_name = re.sub(r'[^A-Za-z0-9|&]', r' ', directory_name).rstrip()
        # directory_name = directory_name.replace("\n", '').replace(":", ' ')
        create_data_files(directory_name)
        set_articles_dir_path('db/'+directory_name+'/articles.txt')
        append_to_existing_file(get_articles_dir_path(), title)
        # print(title)

    # ul = header.find_next('ul').find_all('li', {"class": "entry inproceedings"})
    # for i in ul:
    #     print(i.text)
    # header = soup.findAll('li', {"class": "entry inproceedings"})
    # for a in header:
    #     print(a.text)


# def main():
    # conference_name = 'IEEE Pacific Visualization Symposium'
    # conference_name = 'Conference on Learning Theory (COLT)'
    # conference_name = 'International Joint Conference on Artificial Intelligence (IJCAI)'
    # # conference_name = 'International Conference on Machine Learning (ICML)'
    # year = '2015'
    # searched_result = search_conference([conference_name + ' year:' + year + ':'])
    # # searched_result.to_csv('searchresult.csv', encoding='utf-8')
    # # print(searched_result.iloc[0][1])
    # conference_url = str(searched_result.iloc[0][1])
    # search_articles(conference_url, conference_name)

    # searched_result.to_csv('searchresult.csv', encoding='utf-8')
    # select_conference = searched_result[(searched_result['Title'].str.extract(conference_name))
    #                       & (searched_result['Title'].str.extract(year))]
    # link = select_conference['Link']
    # print(link)

#
# if __name__ == '__main__':
#     main()
