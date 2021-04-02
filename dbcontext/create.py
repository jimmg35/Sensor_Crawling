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
            'projectmeta':'''(
                PROJECTID BIGINT PRIMARY KEY,
                PROJECTNAME TEXT,
                PROJECTKEYS TEXT[]
                );'''
        }
    }
    
    initializer = Constructor(DB_list, DB_details, PGSQLDetail)
    initializer.constructDatabases()
    initializer.constructTables()
    
    
    
    