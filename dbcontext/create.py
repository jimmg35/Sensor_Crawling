from Module.construct import Constructor
import sys


if __name__ == '__main__':
    
    # PostgreSQL server
    PGSQLDetail = {"user":str(sys.argv[1]), 
                "password":str(sys.argv[2]), 
                "host":str(sys.argv[3]), 
                "port":str(sys.argv[4])}
    
    # Databases you want to create
    DB_list = ['sensordata']
    
    # Details of each database
    DB_details = {
        'sensordata':{
            'devicemeta':'''(
                ID BIGINT PRIMARY KEY,
                DEVICEID TEXT,
                PROJECTKEY TEXT,
                PROJECTID TEXT,
                NAME TEXT NULL,
                DESCR TEXT NULL,
                TYPE TEXT NULL,
                LAT TEXT NULL,
                LON TEXT NULL,
                ALT TEXT NULL,
                REFERENCE TEXT NULL,
                DISPLAY TEXT NULL,
                DEVICETYPE TEXT NULL,
                OWNERID TEXT NULL,
                MANUFACTURERID TEXT NULL,
                MANUFACTURERNAME TEXT NULL,
                MOBILE TEXT NULL,
                OUTDOOR TEXT NULL,
                COUNTY TEXT NULL,
                LOCATIONID TEXT NULL,
                URI TEXT NULL,
                UPDATETIME TEXT NULL,
                TAGS TEXT NULL,
                AREA TEXT NULL,
                AREATYPE TEXT NULL,
                AREATYPE_2 TEXT NULL,
                _CHK_LAT_LON TEXT NULL,
                DEVSTAT TEXT NULL,
                ERRORCODE TEXT NULL,
                LANDMARK TEXT NULL,
                MAC_ID TEXT NULL,
                MB_ID TEXT NULL,
                ROAD TEXT NULL,
                SB_ID TEXT NULL,
                TARGET TEXT NULL,
                TOWN TEXT NULL,
                SUBDEVICETYPE TEXT NULL,
                DEVICE_TYPE TEXT NULL,
                ENABLE TEXT NULL,
                PROJECT_ID TEXT NULL,
                ARAETYPE TEXT NULL,
                KEY2 TEXT NULL,
                ADDRESS TEXT NULL,
                HEI TEXT NULL,
                LABEL TEXT NULL,
                LOCATIONID_2 TEXT NULL,
                OWNER TEXT NULL,
                REGION TEXT NULL
                );'''
        }
    }
    
    initializer = Constructor(DB_list, DB_details, PGSQLDetail)
    initializer.constructDatabases()
    initializer.constructTables()
    
    
    
    