import psycopg2 as dbconnector
import pandas as pd


class Db:
    df = pd.read_csv('International Conference on Machine Learning  ICML .csv')
    df = df.drop(df.columns[df.columns.str.contains('unnamed', case=False)], axis=1)

    def __init__(self):
        try:
            connection = dbconnector.connect(user='admin',
                                             password='edgecomps@2019', host='127.0.0.1', port='5432',
                                             database='searchenginedb')
            cursor = connection.cursor()
            table_creation_query = 'CREATE TABLE metadata (ID SERIAL PRIMARY KEY, CONFERENCE TEXT NOT NULL, ' \
                                   'YEAR INT NOT NULL, TITLE TEXT, ABSTRACT TEXT);'
            cursor.execute(table_creation_query)
            connection.commit()
            print('table created')
        except (Exception, dbconnector.Error) as error:
            print("Error while connecting to DB ", error)
        finally:
            if connection:
                # cursor.close()
                connection.close()
                print("DB connection closed")

    def insert_data(self, dataframe):
        try:
            connection = dbconnector.connect(user='admin',
                                             password='edgecomps@2019', host='127.0.0.1', port='5432',
                                             database='searchenginedb')
            cursor = connection.cursor()
            insert_data_query = 'INSERT INTO metadata (CONFERENCE, YEAR, TITLE, ABSTRACT) VALUES (%s, %s, %s, %s)'
            for row in dataframe.itertuples(index=True, name='Pandas'):
                if getattr(row, "title") is not 'none':
                    data_to_insert = (getattr(row, "conference"), str(getattr(row, "year")),
                                      getattr(row, "title"), getattr(row, "abstract"))
                    cursor.execute(insert_data_query, data_to_insert)
                    connection.commit()

        except(Exception, dbconnector.Error) as error:
            print("Error while inserting data to table ", error)

        finally:
            if (connection):
                cursor.close()
                connection.close()
                print('DB connection closed')






