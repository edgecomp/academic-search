import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import euclidean_distances
from sklearn.metrics.pairwise import linear_kernel
from scipy import spatial


def create_collaborative_keyworddb(db):  # counts finger prints of keywords from each conference
    panda_keywords = []
    stop_update_header = False
    header = ['conference']
    for conference_data in db.get_all_data_from_table('conferences_temp'):
        relative_keywords = dict()
        for keyword in db.get_distinct_keywords():
            relative_keywords['conference'] = conference_data[0]
            keyword_df = keyword[0]
            if stop_update_header is False:
                header.append(keyword_df)
            relative_keywords[keyword_df] = conference_data[1].count(keyword_df)
        panda_keywords.append(relative_keywords)
        stop_update_header = True
    return pd.DataFrame(panda_keywords)


# cosine similarity
# def calc_cosine_similarity(X):
#     cosine_sim = linear_kernel(X, X)
#     return cosine_sim


# sklearn euclidean function
# def calc_euclidean_dist(X):
#     eucli_dist = euclidean_distances(X, X)
#     return eucli_dist


# scipy more precise euclidean function
def calc_euclidean_dist(X):
    scipy_eucli_dist = list()
    for index in range(np.size(X, 0)):
        row_list = list()
        for index_2 in range(np.size(X, 0)):
            row_list.append(spatial.distance.euclidean(X[index], X[index_2]))
        scipy_eucli_dist.append(row_list)
    return np.array(scipy_eucli_dist)


def get_neigbors(df):  # extract shortest distance and create dataframe of all conferences' similar conference
    df = df.drop(df.columns[df.columns.str.contains('unnamed', case=False)], axis=1)
    conferences = df['conference']
    df = df.drop(df.columns[df.columns.str.contains('conference', case=False)], axis=1)
    neighbor_conf_index_data = []
    X = df.values
    eucli_dist = calc_euclidean_dist(X)
    min_values = np.where(eucli_dist > 0., eucli_dist, eucli_dist.max()).min(1)
    neighbor_conf_index = [list(eucli_dist[i, :]).index(min_values[i]) for i in range(len(min_values))]
    i = 0
    for conference in conferences:
        neighbor_conf_index_data.append({'conferenceName': conference, 'similar conference': conferences[neighbor_conf_index[i]]})
        i = i + 1
    return pd.DataFrame(neighbor_conf_index_data)
