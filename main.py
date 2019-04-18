import os
import io
import shutil
import conferenceFinder as conf_finder
import dblp_crawler
import scopus_scrapper as sco_scrapper
import time
import re
import pandas as pd


def remove_dir(path):
    shutil.rmtree(path, ignore_errors=True)


def create_project_dir(directory):
    if not os.path.exists(directory):
        print('Creating directory '+directory)
        os.makedirs(directory)


def create_data_files(project_name, base_url):
    create_project_dir(project_name)
    queue = project_name + '/queue.txt'
    crawled = project_name + '/crawled.txt'
    if not os.path.isfile(queue):
        write_file(queue, base_url)
    if not os.path.isfile(crawled):
        write_file(crawled, '')


def write_file(path, data):
    f = open(path, 'w')
    f.write(data)
    f.close()


def append_to_file(path, data):
    with open(path, 'a') as file:
        file.write(data + '\n')


def delete_from_file(path):
    with open(path, 'w'):
        pass


def read_from_file(path):
    return


###
###             TODO: CHANGE STORING DATA INTO OS.FILE TO LIST VARIABLE
###
def main():
    directory_name = 'Conference List'
    remove_dir('db')
    remove_dir(directory_name)
    conference_list = conf_finder.create_list(directory_name)
    conf_finder.get_conference_names(conference_list)
    metadata = []
    year = '2015'

    ################ automated version
    with io.open(conf_finder.CONFERENCE_LIST_DIR_PATH, 'r', encoding='utf-8') as file:
        for line in file:
            conference_name = line

            ######### DONE
            searched_result = dblp_crawler.search_conference([conference_name + ' year:' + year + ':'])
            if not searched_result.empty:
                conference_url = str(searched_result.iloc[0][1])
                dblp_crawler.search_articles(conference_url, conference_name)
                with io.open(dblp_crawler.get_articles_dir_path(), 'r', encoding='utf-8') as fd:
                    for line in fd:
                        print("1" + line)
                        article_name = re.sub("[\(\[].*?[\)\]]", "", line) #remove strings inside brackets
                        article_name_query = re.sub(r'[^A-Za-z0-9|:|-|\']', r' ', article_name)# replace other unwanted character from query
                        print(article_name_query)
                        conference_name_keyword = re.sub(r'[^A-Za-z0-9]', r' ',
                                                         conference_name)  # for checkin article belongs to same conference

                        single_arti_data_in_list = sco_scrapper.scopus_search("TITLE(" + article_name_query + ")",
                                                   conference_name_keyword, conference_name, year)
                        if bool(single_arti_data_in_list) is False:
                            pass
                        else:
                            metadata.append(single_arti_data_in_list)
                pd.DataFrame(metadata).to_csv(conference_name_keyword + year + '.csv', encoding='utf-8', header=True,
                                              columns=['conference', 'year', 'title', 'abstract'])
                metadata = []
            else:
                pass
            # time.sleep(3)
            # metadata = pd.DataFrame(metadata)
            # data = metadata.drop(metadata.columns[metadata.columns.str.contains('unnamed', case=False)], axis=1)

        # metadata = pd.DataFrame(metadata).drop(metadata.columns[metadata.columns.str.contains('unnamed', case=False)], axis=1)
        # metadata.to_csv('metadata.csv', encoding='utf-8', header=True,
        #                           columns=['conference', 'year', 'title', 'abstract'])
    ###########

#     i = 0
#     for conference_name in conference_list:
#         with open('db/'+dir_name[i]+'/articles.txt', 'r', encoding='utf-8') as fd:
#             for line in fd:
#                 print("1" + line)
#                 line = re.sub(r'[^A-Za-z0-9|:|-|\']', r' ', line)
#                 conference_name_keyword = re.sub(r'[^A-Za-z0-9]', r' ', conference_name) #for checkin article belongs to same conference
#                 metadata.append(sco_scrapper.scopus_search("TITLE("+line+")", conference_name_keyword, conference_name, year))
#                 time.sleep(3)
#         i = i + 1
#         pd.DataFrame(metadata).to_csv(conference_name_keyword+'.csv', encoding='utf-8', header=True,
#                                           columns=['conference', 'year', 'title', 'abstract'])
#         metadata = []


    # metadata = []
    # year = '2015'
    # conference_name = 'Conference on Empirical Methods in Natural Language Processing (EMNLP)'
    # with open('db/Conference on Empirical Methods in Natural Language Processing  EMNLP/articles.txt', 'r', encoding='utf-8') as fd:
    #     for line in fd:
    #         print("1" + line)
    #
    #         line = re.sub(r'[^A-Za-z0-9|:|-|\']', r' ', line)
    #         conference_name_keyword = re.sub(r'[^A-Za-z0-9]', r' ',
    #                                          conference_name)  # for checkin article belongs to same conference
    #         metadata.append(
    #             sco_scrapper.scopus_search("TITLE(" + line + ")", conference_name_keyword, conference_name,
    #                                        year))
    # metadata = pd.DataFrame(metadata).drop(metadata.columns[metadata.columns.str.contains('unnamed', case=False)], axis=1)
    # metadata.to_csv('metadata.csv', encoding='utf-8', header=True,
    #                           columns=['conference', 'year', 'title', 'abstract'])


if __name__ == '__main__':
    main()
