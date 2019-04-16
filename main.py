import os
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
    # directory_name = 'Conference List'
    # remove_dir('db')
    # remove_dir(directory_name)
    # conference_list = conf_finder.create_list(directory_name)
    # conf_finder.get_conference_names(conference_list)
    metadata = []
    year = '2015'

    ################# automated version
    # with open(conf_finder.CONFERENCE_LIST_DIR_PATH, 'r', encoding='utf-8') as file:
    #     for line in file:
    #         conference_name = line
    #
    #         ######### DONE
    #         searched_result = dblp_crawler.search_conference([conference_name + ' year:' + year + ':'])
    #         if not searched_result.empty:
    #             conference_url = str(searched_result.iloc[0][1])
    #             dblp_crawler.search_articles(conference_url, conference_name)
    #         else:
    #             pass
    #         with open(dblp_crawler.get_articles_dir_path(), 'r', encoding='utf-8') as fd:
    #             for line in fd:
    #                 print("1" + line)
    #
    #                 line = re.sub(r'[^A-Za-z0-9|:|-]', r' ', line)
    #                 conference_name_keyword = re.sub(r'[^A-Za-z0-9]', r' ',
    #                                                  conference_name)  # for checkin article belongs to same conference
    #                 metadata.append(
    #                     sco_scrapper.scopus_search("TITLE(" + line + ")", conference_name_keyword, conference_name, year))
    #                 time.sleep(3)
    #         pd.DataFrame(metadata).to_csv(conference_name_keyword + '.csv', encoding='utf-8', header=True,
    #                                       columns=['conference', 'year', 'title', 'abstract'])
    #         metadata = []
    ############
    conference_list = ['AAAI Conference on Artificial Intelligence','International Joint Conference on Artificial Intelligence (IJCAI)',
'Conference on Learning Theory (COLT)','International Conference on Artificial Intelligence and Statistics',
                       'Conference on Empirical Methods in Natural Language Processing (EMNLP)',
'Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies (HLT-NAACL)',
'International Conference on Language Resources and Evaluation (LREC)',
'International Conference on Computational Linguistics (COLING)',
'Conference of the European Chapter of the Association for Computational Linguistics (EACL)',
'Conference on Computational Natural Language Learning (CoNLL)',
'International Conference on Computational Linguistics and Intelligent Text Processing',
'International Joint Conference on Natural Language Processing (IJCNLP)',
'ACM SIGGRAPH/Eurographics Symposium on Computer Animation',
'IEEE Pacific Visualization Symposium',
'ACM Symposium on Virtual Reality Software and Technology',
'IEEE Symposium on Visual Analytics Science and Technology',
'Graphics Interface Conference',
'Symposium on Interactive 3D Graphics (SI3D)',
'International Conference on 3D Web Technology',
'IEEE Symposium on Large Data Analysis and Visualization',
'International Conference on Computer Graphics Theory and Applications (GRAPP)',
'IEEE International Solid-State Circuits Conference',
'Design Automation Conference (DAC)',
'Design, Automation and Test in Europe Conference and Exhibition (DATE)',
'IEEE/ACM International Symposium on Microarchitecture',
'International Conference on Computer Aided Verification (CAV)',
'IEEE/ACM International Conference on Computer-Aided Design (ICCAD)',
'IEEE International Symposium on Circuits and Systems',
'Asia and South Pacific Design Automation Conference (ASP-DAC)',
'Symposium on Field Programmable Gate Arrays (FPGA)',
'IEEE Symposium on VLSI Circuits (VLSIC)',
'IEEE International Conference on Computer Communications (INFOCOM)',
'ACM SIGCOMM Conference',
'IEEE International Conference on Communications',
'Annual International Conference on Mobile Computing and Networking',
'ACM Symposium on Computer and Communications Security',
'IEEE Symposium on Security and Privacy',
'USENIX Security Symposium',
'International Cryptology Conference (CRYPTO)',
'Network and Distributed System Security Symposium (NDSS)',
'International Conference on Theory and Applications of Cryptographic Techniques (EUROCRYPT)',
'International Conference on Financial Cryptography and Data Security',
'International Conference on The Theory and Application of Cryptology and Information Security (ASIACRYPT)',
'ACM on Asia Conference on Computer and Communications Security',
'Symposium On Usable Privacy and Security',
'International Conference on Practice and Theory in Public Key Cryptography',
'IEEE Conference on Computer Vision and Pattern Recognition, CVPR',
'IEEE International Conference on Computer Vision',
'European Conference on Computer Vision',
'IEEE Computer Society Conference on Computer Vision and Pattern Recognition Workshops',
'British Machine Vision Conference (BMVC)',
'IEEE International Conference on Image Processing (ICIP)',
'IEEE International Conference on Automatic Face & Gesture Recognition',
'International Conference on Document Analysis and Recognition',
'USENIX Conference on Networked Systems Design and Implementation',
'International Symposium on Computer Architecture (ISCA)',
'International Conference on Architectural Support for Programming Languages and Operating Systems (ASPLOS)',
'IEEE International Symposium on High Performance Computer Architecture',
'IEEE International Symposium on Parallel & Distributed Processing',
'USENIX Annual Technical Conference',
'International Conference for High Performance Computing, Networking, Storage and Analysis',
'ACM European Conference on Computer Systems',
'IEEE/ACM International Symposium on Microarchitecture',
'Conference on File and Storage Technologies (FAST)',
'ACM SIGKDD International Conference on Knowledge Discovery and Data Mining',
'ACM International Conference on Web Search and Data Mining',
'International Conference on Artificial Intelligence and Statistics',
'ACM Conference on Recommender Systems',
'International Conference on Data Mining',
'IEEE International Conference on Big Data',
'SIAM International Conference on Data Mining (SDM)',
'European Conference on Machine Learning and Knowledge Discovery in Databases',
'Pacific-Asia Conference on Knowledge Discovery and Data Mining (PAKDD)',
'International World Wide Web Conferences (WWW)',
'International Conference on Very Large Databases',
'ACM SIGMOD International Conference on Management of Data',
'ACM International Conference on Web Search and Data Mining',
'International Conference on Web and Social Media (ICWSM)',
'International Conference on Data Engineering',
'ACM SIGIR Conference on Research and Development in Information Retrieval',
'ACM International Conference on Information and Knowledge Management',
'International Conference on the Semantic Web',
'ACM Conference on Recommender Systems',
'IEEE International Conference on Big Data',
'ACM International Conference on Multimedia',
'IEEE International Conference on Image Processing (ICIP)',
'ACM International Conference on Multimedia Retrieval',
'International Society for Music Information Retrieval Conference',
'ACM Multimedia Systems Conference (MMSys)',
'IEEE International Conference on Multimedia and Expo',
'IEEE International Conference on Advanced Video and Signal-Based Surveillance (AVSS)',
'IEEE International Conference on Multimedia and Expo Workshops (ICMEW)',
'Conference on Multimedia Modeling',
'IEEE International Conference on Robotics and Automation',
'IEEE/RSJ International Conference on Intelligent Robots and Systems',
'ACM/IEEE International Conference on Human Robot Interaction',
'International Conference on Unmanned Aircraft Systems',
'ACM Symposium on Theory of Computing',
'IEEE Symposium on Foundations of Computer Science (FOCS)',
'ACM SIAM Symposium on Discrete Algorithms',
'Conference on Innovations in Theoretical Computer Science',
'European Symposium on Algorithms',
'Symposium on Theoretical Aspects of Computer Science (STACS)']

    dir_name = ['AAAI Conference on Artificial Intelligence',
'International Joint Conference on Artificial Intelligence  IJCAI',
'Conference on Learning Theory  COLT',
'International Conference on Artificial Intelligence and Statistics',
'Conference on Empirical Methods in Natural Language Processing  EMNLP',
'Conference of the North American Chapter of the Association for Computational Linguistics  Human Language Technologies  HLT NAACL',
'Conference on Computational Natural Language Learning  CoNLL',
'ACM SIGGRAPH Eurographics Symposium on Computer Animation',
'IEEE Pacific Visualization Symposium',
'ACM Symposium on Virtual Reality Software and Technology',
'International Conference on 3D Web Technology',
'IEEE Symposium on Large Data Analysis and Visualization',
'International Conference on Computer Graphics Theory and Applications  GRAPP',
'IEEE International Solid State Circuits Conference',
'Design Automation Conference  DAC',
'IEEE ACM International Conference on Computer Aided Design  ICCAD',
'IEEE International Symposium on Circuits and Systems',
'Asia and South Pacific Design Automation Conference  ASP DAC',
'Symposium on Field Programmable Gate Arrays  FPGA',
'IEEE Symposium on VLSI Circuits  VLSIC',
'ACM SIGCOMM Conference',
'IEEE International Conference on Communications',
'Annual International Conference on Mobile Computing and Networking',
'ACM Symposium on Computer and Communications Security',
'International Cryptology Conference  CRYPTO',
'Network and Distributed System Security Symposium  NDSS',
'International Conference on Theory and Applications of Cryptographic Techniques  EUROCRYPT',
'International Conference on The Theory and Application of Cryptology and Information Security  ASIACRYPT',
'Symposium On Usable Privacy and Security',
'International Conference on Practice and Theory in Public Key Cryptography',
'IEEE Conference on Computer Vision and Pattern Recognition  CVPR',
'IEEE International Conference on Computer Vision',
'IEEE Computer Society Conference on Computer Vision and Pattern Recognition Workshops',
'British Machine Vision Conference  BMVC',
'IEEE International Conference on Image Processing  ICIP',
'IEEE International Conference on Automatic Face & Gesture Recognition',
'International Conference on Document Analysis and Recognition',
'International Symposium on Computer Architecture  ISCA',
'International Conference on Architectural Support for Programming Languages and Operating Systems  ASPLOS',
'IEEE International Symposium on High Performance Computer Architecture',
'International Conference for High Performance Computing  Networking  Storage and Analysis',
'ACM European Conference on Computer Systems',
'Conference on File and Storage Technologies  FAST',
'ACM SIGKDD International Conference on Knowledge Discovery and Data Mining',
'ACM International Conference on Web Search and Data Mining',
'ACM Conference on Recommender Systems',
'International Conference on Data Mining',
'IEEE International Conference on Big Data',
'SIAM International Conference on Data Mining  SDM',
'European Conference on Machine Learning and Knowledge Discovery in Databases',
'ACM SIGMOD International Conference on Management of Data',
'International Conference on Web and Social Media  ICWSM',
'International Conference on Data Engineering',
'ACM SIGIR Conference on Research and Development in Information Retrieval',
'ACM International Conference on Information and Knowledge Management',
'International Conference on the Semantic Web',
'ACM International Conference on Multimedia',
'ACM International Conference on Multimedia Retrieval',
'International Society for Music Information Retrieval Conference',
'ACM Multimedia Systems Conference  MMSys',
'IEEE International Conference on Multimedia and Expo',
'IEEE International Conference on Advanced Video and Signal Based Surveillance  AVSS',
'IEEE International Conference on Robotics and Automation',
'IEEE RSJ International Conference on Intelligent Robots and Systems',
'ACM IEEE International Conference on Human Robot Interaction',
'ACM Symposium on Theory of Computing',
'IEEE Symposium on Foundations of Computer Science  FOCS',
'ACM SIAM Symposium on Discrete Algorithms',
'Conference on Innovations in Theoretical Computer Science',
'Symposium on Theoretical Aspects of Computer Science  STACS']
    i = 0
    for conference_name in conference_list:
        with open('db/'+dir_name[i]+'/articles.txt', 'r', encoding='utf-8') as fd:
            for line in fd:
                print("1" + line)
                line = re.sub(r'[^A-Za-z0-9|:|-|\']', r' ', line)
                conference_name_keyword = re.sub(r'[^A-Za-z0-9]', r' ', conference_name) #for checkin article belongs to same conference
                metadata.append(sco_scrapper.scopus_search("TITLE("+line+")", conference_name_keyword, conference_name, year))
                time.sleep(3)
        i = i + 1
        pd.DataFrame(metadata).to_csv(conference_name_keyword+'.csv', encoding='utf-8', header=True,
                                          columns=['conference', 'year', 'title', 'abstract'])
        metadata = []


if __name__ == '__main__':
    main()
