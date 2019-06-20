import requests
from bs4 import BeautifulSoup

conference_list = list()
items_seen = set()


def set_list(conference):
    conference_list.append(conference)


def set_seen_items(conference):
    items_seen.add(conference)


def get_seen_items():
    return items_seen


def remove_duplicate(conference):  # remove duplicate conferences in different subjects
    if conference not in get_seen_items():
        set_list(conference)
        set_seen_items(conference)


def filter_conferences(conference_name):  # only look for conferences or symposiums
    if 'Conference' in conference_name or 'Symposium' in conference_name:
        remove_duplicate(conference_name)


def get_conference_names():
    subject_names = ['artificialintelligence', 'computationallinguistics', 'computergraphics', 'computerhardwaredesign',
                     'computernetworkswirelesscommunication', 'computersecuritycryptography',
                     'computervisionpatternrecognition', 'computingsystems', 'datamininganalysis',
                     'databasesinformationsystems', 'humancomputerinteraction', 'multimedia', 'robotics',
                     'theoreticalcomputerscience']
    for subject_name in subject_names:
        url = 'https://scholar.google.com/citations?view_op=top_venues&hl=en&vq=eng_%s' % subject_name
        req = requests.get(url)
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')

        tabledata = soup.findAll('td', {"class": "gsc_mvt_t"})
        for singledata in tabledata:
            conference_name = singledata.text
            filter_conferences(conference_name)
    return conference_list
