
# Author : @jimmg35

import datetime
import schedule
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

class UrlBundler():
    """
        Url library for the project.
    """
    base_url = r"https://iot.epa.gov.tw"
    getProjects: str = base_url + r"/iot/v1/project"
    getDevicesOfProj: str = base_url + r"/iot/v1/device"


class Key():
    """
        key class for api authentication.
    """
    key: str = 'AK39R4UXH52FXA9CPA'


class Storer():
    """
        Storing processed data from Parser.
    """
    data_list = []
    storage = {}
    def __init__(self, dbcontext):
        self.dbcontext = dbcontext

    def insert(self, data, name: str):
        self.storage[name] = data
        self.data_list.append(name)

    def import2Database(self, item: str):
        if item == "ProjectData" and self.data_list.index(item) != 1:
            self.dbcontext.ImportProjectMeta(self.storage[item])
            




class Dbcontext():
    """
        Importing data into database.
    """   
    def __init__(self, PGSQL_user_data, database):
        # PostgreSQL server variable.
        self.PGSQL_user_data = PGSQL_user_data
        # Connect to local Postgresql server.
        self.cursor = self.ConnectToDatabase(database)
            
    def ConnectToDatabase(self, database):
        conn = psycopg2.connect(database=database, 
                                user=self.PGSQL_user_data["user"],
                                password=self.PGSQL_user_data["password"],
                                host=self.PGSQL_user_data["host"],
                                port=self.PGSQL_user_data["port"])
        conn.autocommit = True
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        print(f'Successfully connected to local PostgreSQL server| User: @{self.PGSQL_user_data["user"]}')
        print(f'                        Currently connected to database: @{database}')
        cursor = conn.cursor()
        return cursor 

    def ImportProjectMeta(self, projectMeta):
        for projID in list(projectMeta.keys()):
            keys_arr: str = "'{"
            for index, i in enumerate(projectMeta[projID]["keys"]):
                if index == (len(projectMeta[projID]["keys"])-1):
                    keys_arr += '"' + i + '"' + "}'"
                else:
                    keys_arr += '"' + i + '"' + ','


            query = '''INSERT INTO projectmeta (projectid, projectname, projectkeys) 
                                VALUES({}, \'{}\', {});'''.format(str(projID), 
                                                                  projectMeta[projID]["name"],
                                                                  keys_arr)
            self.cursor.execute(query)
        print("Project Metadata has been stored into database!")