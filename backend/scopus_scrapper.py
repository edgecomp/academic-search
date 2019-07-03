import requests
import re
from bs4 import BeautifulSoup
from time import sleep

SCOPUS_SEARCH_BASE = 'https://api.elsevier.com/content/search/scopus?query='
SCOPUS_ABSTRACT_SEARCH_BASE = 'https://api.elsevier.com/content/abstract/eid/'
SCOPUS_ABSTRACT_QUERY_CONDI = '?view=FULL&'
entry_index = 0
apikeys = ['71acdba5a5f79df2ba573f30c8ecec5e', '8bac7f9b7848efc81035b350bf8b7d38', 'd95c8b33fa311482fbf8760075ba84b4',
           '3e0d9e761193aaa3554460173e3f74e3', '65d7d726d89e7b26b19bd56dacd4f097', 'cf5ad9c3324c6dcb4136ae57973b6109',
           'a6c044a053fb2a420e6519e6be1c4384', '22c2823cd1f58c3bb988d37cdf1c7fec',
           'a8fc32fade6892e024cc4eb1da5e7685', 'a82e43fef3fb8f6eaff886c3468f3fa8']
proxies = {'https': "socks5://localhost:8000"}  # For ssh tunneling


def get_api_key(apikey_index):
    apikey = '&apikey=' + apikeys[apikey_index]
    return apikey


def set_index(index_toset):
    global entry_index
    entry_index = index_toset


def get_index():
    return entry_index


def string_contains(crawled_publname, publname):  # crawled publi name contains publi name in interest
    if crawled_publname:
        if publname in crawled_publname:
            return True
    else:
        return False


def process_crawled_publname(element): # remove non-alphanumeric char from publication name
    if 'prism:publicationName' in element:
        crawled_publname = re.sub("[\(\[].*?[\)\]]", "", element['prism:publicationName'])
        crawled_publname = re.sub(r'[^A-Za-z0-9]', r' ', crawled_publname)
        crawled_publname = crawled_publname.lower()
        return crawled_publname
    else:
        return ''


def no_matching_result(search_results, conference_name):
    index = 0
    if nr_result_found(search_results) >= 1:   # if multiple items found search compare conference name
        if ('search-results' in search_results) and ('entry' in search_results['search-results']):
            for element in search_results['search-results']['entry']:
                if string_contains(process_crawled_publname(element), conference_name.lower()):
                    set_index(index)
                    return False
                else:
                    index = index + 1
    return True


def no_result_found(nr_results):
    if nr_results == 0:
        return True
    else:
        return False


def nr_result_found(search_results):
    if ('search-results' in search_results) and ('opensearch:totalResults' in search_results['search-results']):
        nr_results = search_results['search-results']['opensearch:totalResults']
        return int(float(nr_results))
    else:
        return 0  # case handling dict keys not found


def scrape_article_data(search_result_url, conference_name_keyword, conference_name, year, key_index):
    set_index(0)
    search_results = requests.get(search_result_url).json()
    if no_result_found(nr_result_found(search_results) or
                       no_matching_result(search_results, conference_name_keyword)):
        return None
    else:
        if 'eid' in search_results['search-results']['entry'][get_index()]:
            article_in_interest_eid = search_results['search-results']['entry'][get_index()]['eid']
            abstract_url = SCOPUS_ABSTRACT_SEARCH_BASE + article_in_interest_eid + \
                           SCOPUS_ABSTRACT_QUERY_CONDI + get_api_key(key_index)
            article_in_interest = requests.get(abstract_url, proxies=proxies, verify=False) # verify=False to avoid Max retries exceeded error
            sleep(1)
            soup = BeautifulSoup(article_in_interest.content, 'xml')
            title = soup.find('dc:title')
            abstract = soup.find('ce:para')
            if title is None or abstract is None:  # pass if either data missing
                return None
            else:
                title = title.text
                abstract = abstract.text
                return {'conference_type': conference_name, 'year': year, 'title': title, 'abstract': abstract}
        else:
            return None


def scopus_search(query, conference_name_keyword, conference_name, year, key_index):
    search_result_url = SCOPUS_SEARCH_BASE + query + get_api_key(key_index)
    return scrape_article_data(search_result_url, conference_name_keyword, conference_name, year, key_index)
