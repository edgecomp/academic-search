import os
import requests
from bs4 import BeautifulSoup


def create_conference_list_dir(directory_name):
    if not os.path.exists(directory_name):
        print('Creating directory '+directory_name+' .......')
        os.makedirs(directory_name)


def create_list(project_directory):
    create_conference_list_dir(project_directory)
    conference_list = project_directory + '/conference_list.txt'
    if not os.path.isfile(conference_list):
        write_file(conference_list, '')
    return conference_list


def write_file(path, data):
    fd = open(path, 'w')
    fd.write(data)
    fd.close()


def append_to_existing_file(path, data):
    with open(path, 'a') as fd:
        fd.write(data + '\n')


def filter_conferences(conference_name, list_path):
    if 'Conference' in conference_name or 'Symposium' in conference_name:
        # print(conference_name)
        append_to_existing_file(list_path, conference_name)


def get_conference_names(list_path):
    subject_names = ['artificialintelligence', 'computationallinguistics', 'computergraphics', 'computerhardwaredesign',
                     'computernetworkswirelesscommunication', 'computersecuritycryptography',
                     'computervisionpatternrecognition', 'computingsystems', 'datamininganalysis',
                     'databasesinformationsystems', 'humancomputerinteractioin', 'multimedia', 'robotics',
                     'theoreticalcomputerscience']
    for subject_name in subject_names:
        url = 'https://scholar.google.com/citations?view_op=top_venues&hl=en&vq=eng_%s' % subject_name
        req = requests.get(url)
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')

        tabledatas = soup.findAll('td', {"class": "gsc_mvt_t"})
        for tableData in tabledatas:
            conference_name = tableData.text
            filter_conferences(conference_name, list_path)


def main():
    directory_name = 'Conference List'
    # create_conference_list_dir(directory_name)
    get_conference_names(create_list(directory_name))


if __name__ == "__main__":
    main()
