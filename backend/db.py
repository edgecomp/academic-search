import psycopg2 as pgdb2


# queries to execute before calling DB class

# 'CREATE TABLE conferences (CONFERENCE_NAME TEXT NOT NULL PRIMARY KEY, CORPUS TEXT NOT NULL, SIMILAR_CONFERENCE TEXT);'
# 'CREATE TABLE conferences_temp (CONFERENCE_NAME TEXT NOT NULL PRIMARY KEY, CORPUS TEXT NOT NULL, SIMILAR_CONFERENCE TEXT);'

# 'CREATE TABLE metadata (ID SERIAL PRIMARY KEY, CONFERENCE_TYPE TEXT NOT NULL, YEAR INT NOT NULL, TITLE TEXT, ABSTRACT TEXT, CONFERENCE_NAME TEXT REFERENCES conferences (CONFERENCE_NAME));'
# 'CREATE TABLE metadata_temp (ID SERIAL PRIMARY KEY, CONFERENCE_TYPE TEXT NOT NULL, YEAR INT NOT NULL, TITLE TEXT, ABSTRACT TEXT, CONFERENCE_NAME TEXT REFERENCES conferences_temp (CONFERENCE_NAME));'

# 'CREATE TABLE keywords (KEYWORD TEXT NOT NULL, SCORE DOUBLE PRECISION NOT NULL, CONFERENCE_NAME TEXT REFERENCES conferences (CONFERENCE_NAME));'
# 'CREATE TABLE keywords_temp (KEYWORD TEXT NOT NULL, SCORE DOUBLE PRECISION NOT NULL, CONFERENCE_NAME TEXT REFERENCES conferences_temp (CONFERENCE_NAME));'


NONE_CONFERENCETYPE_CHAR_NR = -5
YEAR_CHARACTER_NR = -4


class DB:

    def __init__(self):
        try:
            self.connec = pgdb2.connect(user='admin',
                                             password='edgecomps@2019', host='127.0.0.1', port='5432',
                                             database='searchenginedb')
            self.cur = self.connec.cursor()
        except (Exception, pgdb2.Error) as error:
            print("Error while connecting to DB ", error)
    #
    # def insert_data(self, insert_data_query, data_to_insert):
    #     try:
    #         self.cur.execute(insert_data_query, data_to_insert)
    #         self.connec.commit()
    #     except(Exception, pgdb2.Error) as error:
    #         self.connec.rollback()
    #         print("Error while inserting data to table ", error)

    # TODO remove
    # def insert_metadata(self, datadict):
    #     try:
    #         insert_data_query = 'INSERT INTO metadata (CONFERENCE_TYPE, YEAR, TITLE, ABSTRACT) VALUES (%s, %s, %s, %s)'
    #         data_to_insert = (datadict.get("conference_type"), str(datadict.get("year")),
    #                           datadict.get("title"), datadict.get("abstract"))
    #         self.cur.execute(insert_data_query, data_to_insert)
    #         self.connec.commit()
    #     except(Exception, pgdb2.Error) as error:
    #         self.connec.rollback()
    #         print("Error while inserting data to table ", error)
    # ###########################

    def insert_allmetadata(self, dataframe):
        try:
            insert_data_query = 'INSERT INTO metadata_temp (CONFERENCE_TYPE, YEAR, TITLE, ABSTRACT) VALUES (%s, %s, %s, %s)'
            for row in dataframe.itertuples(index=True, name='Pandas'):
                if getattr(row, "title") is not 'none':
                    data_to_insert = (getattr(row, "conference_type"), str(getattr(row, "year")),
                                      getattr(row, "title"), getattr(row, "abstract"))
                    self.cur.execute(insert_data_query, data_to_insert)
                    self.connec.commit()
        except(Exception, pgdb2.Error) as error:
            self.connec.rollback()
            print("Error while inserting dataframe to table metadata ", error)

    def insert_keyworddata(self, keyworddict):
        try:
            insert_data_query = 'INSERT INTO keywords_temp (CONFERENCE_NAME, KEYWORD, SCORE) VALUES (%s, %s, %s)'
            data_to_insert = (keyworddict.get("conference"), keyworddict.get("keyword"),
                              float(keyworddict.get("score")))
            self.cur.execute(insert_data_query, data_to_insert)
            self.connec.commit()
        except(Exception, pgdb2.Error) as error:
            self.connec.rollback()
            print("Error while inserting data to table ", error)

    def insert_conference(self, corpus_dict):
        try:
            insert_data_query = 'INSERT INTO conferences_temp (CONFERENCE_NAME, CORPUS) VALUES (%s, %s)'
            data_to_insert = (corpus_dict.get("conference_name"), corpus_dict.get("corpus"))
            self.cur.execute(insert_data_query, data_to_insert)
            self.connec.commit()
        except(Exception, pgdb2.Error) as error:
            self.connec.rollback()
            print("Error while inserting dataframe to table ", error)

    #TODO REMOVE
    ########################################################################
    # def insert_allconferences(self, dataframe):
    #     try:
    #         insert_data_query = 'INSERT INTO conferences (CONFERENCE_NAME, CORPUS) VALUES (%s, %s)'
    #         for row in dataframe.itertuples(index=True, name='Pandas'):
    #             data_to_insert = (getattr(row, "conference_name"), getattr(row, "corpus"))
    #             self.cur.execute(insert_data_query, data_to_insert)
    #             self.connec.commit()
    #     except(Exception, pgdb2.Error) as error:
    #         self.connec.rollback()
    #         print("Error while inserting dataframe to table ", error)
    #################################################################################

    def insert_allkeywords(self, dataframe):
        try:
            insert_data_query = 'INSERT INTO keywords_temp (KEYWORD, SCORE, CONFERENCE_NAME) VALUES (%s, %s, %s)'
            for row in dataframe.itertuples(index=True, name='Pandas'):
                data_to_insert = (getattr(row, "keyword"),
                                  float(getattr(row, "score")), getattr(row, "conferenceName"))
                self.cur.execute(insert_data_query, data_to_insert)
                self.connec.commit()
        except(Exception, pgdb2.Error) as error:
            self.connec.rollback()
            print("Error while inserting dataframe to table ", error)

    def truncate_table(self, tablename):
        try:
            truncate_data_query = 'TRUNCATE TABLE ' + tablename + ' RESTART IDENTITY CASCADE'
            self.cur.execute(truncate_data_query)
            self.connec.commit()
        except(Exception, pgdb2.Error) as error:
            self.connec.rollback()
            print("Error while truncating table", error)

    # def get_metadata_abstract(self, crawled_datadict):
    #     try:
    #         get_data_query = 'SELECT abstract FROM metadata WHERE CONFERENCE_TYPE = %s AND YEAR = %s AND TITlE = %s'
    #         data_to_retrive_condi = (crawled_datadict.get("conference"), crawled_datadict.get("year"),
    #                                  crawled_datadict.get("title"))
    #         self.cur.execute(get_data_query, data_to_retrive_condi)
    #         return self.cur.fetchone()
    #     except(Exception, pgdb2.Error) as error:
    #         print("Error while retrieving data from table", error)
    #############
    # def get_confname_abstract_from_metadata(self):
    #     try:
    #         get_data_query = 'SELECT CONFERENCE_TYPE, YEAR, ABSTRACT FROM metadata_temp'
    #############

    def get_all_data_from_table(self, tablename):
        try:
            get_data_query = 'SELECT * FROM ' + tablename
            self.cur.execute(get_data_query)
            return self.cur.fetchall()
        except(Exception, pgdb2.Error) as error:
            print("Error while retrieving data from table", error)

    def get_distinct_keywords(self):
        try:
            get_data_query = 'SELECT DISTINCT keyword FROM keywords_temp'
            self.cur.execute(get_data_query)
            return self.cur.fetchall()
        except(Exception, pgdb2.Error) as error:
            print("Error while retrieving data from table", error)

    def update_metadata(self, conference_name):
        try:
            update_query = 'UPDATE metadata_temp SET CONFERENCE_NAME = %s WHERE CONFERENCE_TYPE = %s AND YEAR = %s'
            global NONE_CONFERENCETYPE_CHAR_NR, YEAR_CHARACTER_NR
            conference_type = conference_name[:NONE_CONFERENCETYPE_CHAR_NR]
            year = conference_name[YEAR_CHARACTER_NR:]
            data = (conference_name, conference_type, int(float(year)))
            self.cur.execute(update_query, data)
            self.connec.commit()
        except(Exception, pgdb2.Error) as error:
            self.connec.rollback()
            print("Error while updating data to table", error)

    def update_conferencestemp_table(self, neighbor, conference_name):
        try:
            update_query = 'UPDATE conferences_temp SET similar_conference = %s WHERE CONFERENCE_NAME = %s'
            data = (neighbor, conference_name)
            self.cur.execute(update_query, data)
            self.connec.commit()
        except(Exception, pgdb2.Error) as error:
            self.connec.rollback()
            print("Error while updating data to table", error)

    # def update_keywords_table(self, neighbor, conference_name):
    #     try:
    #         update_query = 'UPDATE keywords_temp SET NEIGHBOR = %s WHERE CONFERENCE_NAME = %s'
    #         data = (neighbor, conference_name)
    #         self.cur.execute(update_query, data)
    #         self.connec.commit()
    #     except(Exception, pgdb2.Error) as error:
    #         self.connec.rollback()
    #         print("Error while updating data to table", error)

    # def alter_keywords_table(self):
    #     try:
    #         alter_query = 'ALTER TABLE keywords ADD COLUMN neighbor TEXT'
    #         self.cur.execute(alter_query)
    #         self.connec.commit()
    #     except (Exception, pgdb2.Error) as error:
    #         print("Error while altering table", error)

    def copy_data_to_another_table(self, des_table, temp_table):
        try:
            copy_query = 'INSERT INTO ' + des_table + ' SELECT * FROM ' + temp_table
            self.cur.execute(copy_query)
            self.connec.commit()
        except (Exception, pgdb2.Error) as error:
            print("Error while copying table", error)

    # def terminate(self):
    #     try:
    #         self.cur.close()
    #         self.connec.close()
    #     except(Exception, pgdb2.Error) as error:
    #         print("Error while closing the DB", error)
