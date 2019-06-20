import requests
import pandas as pd
from bs4 import BeautifulSoup

DBLP_BASE_URL = 'http://dblp.uni-trier.de/'
PUB_SEARCH_URL = DBLP_BASE_URL + "search/publ/"


def build_query(search_string):
    request = requests.get(PUB_SEARCH_URL, params={'q': search_string})
    return BeautifulSoup(request.content, 'html.parser')


def scrape_conference(search_string):  # scrapes conference
    try:
        soup = build_query(search_string)
        pub = soup.findAll("li", {"class": "entry editor toc"})
        pub_list_data = []
        for li in pub:
            link = 'nothing'
            authors = []
            title = 'nothing'
            data = li.find("div", {"class": "data"})
            authors_data = data.findAll('span', attrs={"itemprop": "author"})
            for author in authors_data:
                authors.append(author.text)
            title = data.find('span', {"class": "title"}).text
            publ = li.find("nav", {"class": "publ"})
            link_div = publ.find("div", {"class": "head"})
            link = link_div.find("a").get("href")
            pub_data = {'Link': link, 'Authors': authors, 'Title': title}
            pub_list_data.append(pub_data)
        return pd.DataFrame(pub_list_data)
    except Exception as excep:
        print(excep)
    finally:
        pass


def scrape_articles(conference_doc_url):     # scrapes articles from one conference
    try:
        request = requests.get(conference_doc_url)
        soup = BeautifulSoup(request.content, 'html.parser')
        lis = soup.findAll('li', {"class": "entry inproceedings"})
        article_list = list()
        for li in lis:
            data = li.find("div", {"class": "data"})
            title = data.find('span', {"class": "title"}).text
            article_list.append(title)
        return article_list
    except requests.exceptions as excep:
        print(excep)
    finally:
        pass
