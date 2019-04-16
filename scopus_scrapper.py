from bs4 import BeautifulSoup
import requests
import time
import re
from sshtunnel import SSHTunnelForwarder


# scopus API Key 5a3078ff1f78d91130566929c2721e44
#
# server = SSHTunnelForwarder(
#     'ssh.data.vu.nl',
#     ssh_username='',
#     ssh_password='',
#     remote_bind_address=('127.0.0.1', 8080)
# )
#
SCOPUS_SEARCH_BASE = 'https://api.elsevier.com/content/search/scopus?query='
entry_index = 0


def get_api_key():
    apikey = '&apikey=5a3078ff1f78d91130566929c2721e44'
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
        # for element in search_results['search-results']['entry']:
        #     a = element['dc:title'].split()
        #     b = keyword.split()
            if string_contains(crawled_publname, publname) is False:
            # if element['dc:title'] != keyword:  # match not found
                # print(element['dc:title'])
                # print(keyword)
                index = index+1
            else:
                set_index(index)
                return False
        return True


def scrape_article_data(search_result_url, conference_name_keyword, conference_name, year):
    search_results = requests.get(search_result_url).json()
    # time.sleep(2)
    if no_result_found(nr_result_found(search_results)) is True \
            or no_matching_result(search_results, conference_name_keyword) is True:
        title = "None"
        # print(title)
        abstract = "None"
        # print(abstract)
    else:
        # print("a")
        doc_page_url = search_results['search-results']['entry'][get_index()]['link'][2]['@href']
        # print(doc_page_url)
        time.sleep(3)
        doc_page = requests.get(str(doc_page_url) + get_api_key())
        soup = BeautifulSoup(doc_page.text, 'html.parser')
        title = soup.find('h2', {"class": "h3"})
        print(title)
        unwanted_text = title.find('span')
        if unwanted_text is not None:
            unwanted_text.extract()
            title = title.text.strip()
        else:
            title = title.text
        abstract_section = soup.find('section', {"id": "abstractSection"})
        abstract = abstract_section.find('p').text
        # print("output: "+title)
        # print(abstract)
    return {'conference': conference_name, 'year': year, 'title': title, 'abstract': abstract}


def scopus_search(query, conference_name_keyword, conference_name, year):
    # server.start()
    # query = 'TITLE(Stochastic Optimization with Importance Sampling for Regularized Loss Minimization.)'
    # query = 'TITLE(Bayesian Multiple Target Localization.)'
    # query='TITLE(Distributed Gaussian Processes.)'
    search_result_url = SCOPUS_SEARCH_BASE + query + get_api_key()
    return scrape_article_data(search_result_url, conference_name_keyword, conference_name, year)

# asd = requests.get(a['link'][2]['@href']+ apikey)
# print(asd.text)
# json.load(asd)


# a = search_data['search-results']['entry'][0]['prism:url']
# b = requests.get(a).content
# print(b)


# json_data = search_data.json()
# print(json_data)

# with open('d_json.json', 'w') as fd:
#     json.dump(json_data, fd)


# scopus.utils.create_config()
# s = ScopusSearch(query, refresh=True)
# print(s.results)
# df = pd.DataFrame(pd.DataFrame(s.results))
# df.to_csv('scopus.csv', encoding='utf-8')
# eids = s.get_eids()
# print(eids)

# server.stop()
# keyword = 'Stochastic Optimization with Importance Sampling for Regularized Loss Minimization.'
# scopus_search('TITLE(' + keyword + ')', keyword)


# conference_name = 'International Conference on Machine Learning (ICML)'
# with open('International Conference on Machine Learning (ICML)/articles.txt', 'r', encoding='utf-8') as fd:
#     for line in fd:
#         print("1" + line)
#         line = re.sub(r'[^A-Za-z0-9|:|-]', r' ', line)
#         conference_name = re.sub(r'[^A-Za-z0-9]', r' ', conference_name)
#         scopus_search("TITLE("+line+")", conference_name)
#         time.sleep(0.5)
