
# Author : @jimmg35

import datetime
import schedule
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


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
        if item == "ProjectData" and self.importGate(item):
            self.dbcontext.ImportProjectMeta(self.storage[item])
        if item == "DeviceMeta" and self.importGate(item):
            self.dbcontext.ImportDeviceMeta(self.storage[item])
        if item == "SensorMeta" and self.importGate(item):
            self.dbcontext.ImportSensorMeta(self.storage[item])
    
    def importGate(self, item):
        if self.data_list.index(item) != -1:
            return True
        else:
            print("Data is not accessible!")
            return False


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
                    keys_arr += '"' + str(i) + '"' + "}'"
                    break
                keys_arr += '"' + str(i) + '"' + ','
            query = '''INSERT INTO projectmeta (projectid, projectname, projectkeys) 
                                VALUES({}, \'{}\', {});'''.format(str(projID), 
                                                                  projectMeta[projID]["name"],
                                                                  keys_arr)
            self.cursor.execute(query)
        print("Project Metadata has been stored into database!")
    
    def ImportDeviceMeta(self, deviceMeta):
        column_str = "("
        query = "select column_name from information_schema.columns where table_name = 'devicemeta';"
        self.cursor.execute(query)
        column = [i[0] for i in self.cursor.fetchall()]
        for index, i in enumerate(column):
            if index == (len(column)-1):
                column_str += i + ")"
                break
            column_str += i + ","
        for index, i in enumerate(deviceMeta):
            values = self.bulidDeviceMetaQuery(i, index)
            query = "INSERT INTO devicemeta " + column_str + values
            self.cursor.execute(query)
        print("Device Metadata has been stored into database!")

    def ImportSensorMeta(self, SensorMeta):
        ids = 1
        
        
        for device in SensorMeta:
            sensor_id = "'{"
            for index, i in enumerate(device[2]):
                if index == (len(device[2])-1):
                    sensor_id += '"' + str(i) + '"' + "}'"
                    break
                sensor_id += '"' + str(i) + '"' + ','
            query = '''INSERT INTO sensormeta (id, deviceid, projectkey, sensor_id)
                        VALUES({}, \'{}\', \'{}\', {});'''.format(ids, device[0], device[1], sensor_id)
            self.cursor.execute(query)
            ids += 1
        print("Sensor Metadata has been stored into database!")


    def bulidDeviceMetaQuery(self, device, count):
        output = " VALUES(" + str(count) + "," + device["id"] + ","
        for index, i in enumerate(list(device.keys())):
            if index == (len(list(device.keys())) - 1):
                output += "'" + str(device[i]) + "')"
                break
            if i == "id":
                continue
            if str(device[i]) == "旗山區公所前'":
                output += "'" + "旗山區公所前" + "',"
                continue
            output += "'" + str(device[i]) + "',"
        return output
    
    def launchPatch(self):
        queries = ['''DELETE FROM devicemeta WHERE projectid 
                    NOT IN ('528','671','672','673','674',
                    '675','677','678','680','709',
                    '756','1024','1025','1027','1029',
                    '1032','1034','1035','1036','1048',
                    '1058','1071','1072','1075','1079',
                    '1084','1085','1102','1120','1145',
                    '1147','1162','1167','1184','1189',
                    '1192','1207','1156','565','624','891');''']
        for index, i in enumerate(queries):
            print("Patch {} has been applied to database!".format(index))
            self.cursor.execute(i)