import requests
import re
from bs4 import BeautifulSoup
# from sshtunnel import SSHTunnelForwarder

#https://api.elsevier.com/content/abstract/eid/2-s2.0-84984674681?view=FULL&&apikey=289699373eeaaa4f37973f4abd455ddf

SCOPUS_SEARCH_BASE = 'https://api.elsevier.com/content/search/scopus?query='
SCOPUS_ABSTRACT_SEARCH_BASE = 'https://api.elsevier.com/content/abstract/eid/'
SCOPUS_ABSTRACT_QUERY_CONDI = '?view=FULL&'
entry_index = 0


def get_api_key():
    apikey = '&apikey=de1e502e55a0c85e91b0ff562a757e3a'
    return apikey


def nr_result_found(search_results):
    nr_results = search_results['search-results']['opensearch:totalResults']
    return int(float(nr_results))


def no_result_found(nr_results):
    # print(nr_results)
    if nr_results == 0:
        return True
    else:
        return False


def set_index(index_toset):
    global entry_index
    entry_index = index_toset


def get_index():
    return entry_index


def string_contains(list_input, list_to_compare):
    matched = 0
    for item_input in list_input:
        for item_to_compare in list_to_compare:
            if item_to_compare.lower() == item_input.lower():
                # print(item_to_compare.lower())
                # print(item_input.lower())
                matched = matched+1
    if matched == len(list_to_compare):
        return True
    else:
        # print(matched)
        # print(len(list_to_compare))
        return False


def no_matching_result(search_results, conference_name):
    index = 0
    set_index(0)
    if nr_result_found(search_results) > 1:
        for element in search_results['search-results']['entry']:
            crawled_publname = re.sub(r'[^A-Za-z0-9]', r' ', element['prism:publicationName'])
            crawled_publname = crawled_publname.split()
            # crawled_publname = element['prism:publicationName'].split()
            publname = conference_name.split()
            # print(crawled_publname)
            # print(publname)
            if string_contains(crawled_publname, publname) is False:
                index = index+1
            else:
                set_index(index)
                return False
        return True


def scrape_article_data(search_result_url, conference_name_keyword, conference_name, year):
    search_results = requests.get(search_result_url).json()
    # time.sleep(1)
    if no_result_found(nr_result_found(search_results)) is True \
            or no_matching_result(search_results, conference_name_keyword) is True:
        # title = ""
        # print(title)
        # abstract = ""
        # print(abstract)
        return {}
    else:
        ###################### SSH TUNNELING TO REMOVE AFTER IMPLEMENTATION
        # server = SSHTunnelForwarder(
        #     'ssh.data.vu.nl',
        #     ssh_username='',
        #     ssh_password='',
        #     remote_bind_address=('127.0.0.1', 1080)
        # )
        # server.start()
        ######################################################
        article_in_interest_eid = search_results['search-results']['entry'][get_index()]['eid']
        abstract_url = SCOPUS_ABSTRACT_SEARCH_BASE + article_in_interest_eid + SCOPUS_ABSTRACT_QUERY_CONDI + get_api_key()
        # print(abstract_url)
        article_in_interest = requests.get(abstract_url)
        soup = BeautifulSoup(article_in_interest.content, 'xml')
        print(soup)
        # data = article_in_interest.text
        # title = data['abstracts-retrieval-response']['coredata']['prism:publicationName']
        # abstract = data['abstracts-retrieval-response']['coredata']['dc:description']['abstract']['ce:para']
        title = soup.find('dc:title')
        if title is None:
            title = ''
        else:
            title = title.text

        abstract = soup.find('ce:para')
        if abstract is None:
            abstract = ''
        else:
            abstract = abstract.text
        print(abstract)
        # server.close()
        # print("output: "+title)
        # print(abstract)
        return {'conference': conference_name, 'year': year, 'title': title, 'abstract': abstract}


def scopus_search(query, conference_name_keyword, conference_name, year):
    search_result_url = SCOPUS_SEARCH_BASE + query + get_api_key()
    return scrape_article_data(search_result_url, conference_name_keyword, conference_name, year)
