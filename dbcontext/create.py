from Module.construct import Constructor
import sys


build_tables = {}

projects = ['528','671','672','673','674','675',
            '677','678','680','709','756','1024','1025',
            '1027','1029','1032','1034','1035','1036',
            '1048','1058','1071','1072','1075','1079',
            '1084','1085','1102','1120','1145','1147',
            '1162','1167','1184','1189','1192','1207']
for i in projects:
    build_tables["minute_"+i] = '''(ID BIGINT PRIMARY KEY,
                                        DEVICEID TEXT,
                                        PM2_5_AVG DOUBLE PRECISION,
                                        PM2_5_MAX DOUBLE PRECISION,
                                        PM2_5_MIN DOUBLE PRECISION,
                                        PM2_5_MEDIAN DOUBLE PRECISION,
                                        HUMIDITY_AVG DOUBLE PRECISION,
                                        HUMIDITY_MAX DOUBLE PRECISION,
                                        HUMIDITY_MIN DOUBLE PRECISION,
                                        HUMIDITY_MEDIAN DOUBLE PRECISION,
                                        TEMPERATURE_AVG DOUBLE PRECISION,
                                        TEMPERATURE_MAX DOUBLE PRECISION,
                                        TEMPERATURE_MIN DOUBLE PRECISION,
                                        TEMPERATURE_MEDIAN DOUBLE PRECISION,
                                        YEAR INT,
                                        MONTH INT,
                                        DAY INT,
                                        HOUR INT,
                                        MINUTE INT,
                                        SECOND INT,
                                        TIME TIMESTAMP);'''
    build_tables["hour_"+i] = '''(ID BIGINT PRIMARY KEY,
                                        DEVICEID TEXT,
                                        PM2_5_AVG DOUBLE PRECISION,
                                        PM2_5_MAX DOUBLE PRECISION,
                                        PM2_5_MIN DOUBLE PRECISION,
                                        PM2_5_MEDIAN DOUBLE PRECISION,
                                        HUMIDITY_AVG DOUBLE PRECISION,
                                        HUMIDITY_MAX DOUBLE PRECISION,
                                        HUMIDITY_MIN DOUBLE PRECISION,
                                        HUMIDITY_MEDIAN DOUBLE PRECISION,
                                        TEMPERATURE_AVG DOUBLE PRECISION,
                                        TEMPERATURE_MAX DOUBLE PRECISION,
                                        TEMPERATURE_MIN DOUBLE PRECISION,
                                        TEMPERATURE_MEDIAN DOUBLE PRECISION,
                                        YEAR INT,
                                        MONTH INT,
                                        DAY INT,
                                        HOUR INT,
                                        MINUTE INT,
                                        SECOND INT,
                                        TIME TIMESTAMP);'''




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
        'sensordata':build_tables
    }
    
    initializer = Constructor(DB_list, DB_details, PGSQLDetail)
    initializer.constructDatabases()
    initializer.constructTables()
    
    
    
    