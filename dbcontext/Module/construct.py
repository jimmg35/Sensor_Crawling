import time
import hmac
import base64
import datetime
import schedule
import psycopg2
from time import mktime
from hashlib import sha1
from pprint import pprint
from requests import request
from datetime import datetime
from wsgiref.handlers import format_date_time
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT



class Constructor():
    def __init__(self, DB_list, DB_detail, PGSQLDetail):
        # Databases need to be constructed
        self.DB_list = DB_list
        
        # Information of Databases and Tables
        self.DB_detail = DB_detail
        
        # PostgreSQL server variable
        self.user = PGSQLDetail['user']
        self.password = PGSQLDetail['password']
        self.host = PGSQLDetail['host']
        self.port = PGSQLDetail['port']
        
        # Connect to PostgreSQL
        self.cursor = self.ConnectToPGSQL(self.user, self.password, self.host, self.port)
        
        # Kill query
        self.Kill = '''SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE pid <> pg_backend_pid() AND datname = 'template1';'''
    
    def ConnectToPGSQL(self, user, password, host, port):
        
        '''Connect to PostgreSQL'''
        
        conn = psycopg2.connect(user=user,password=password,host=host,port=port)
        conn.autocommit = True
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        print(f'Successfully connected | User:{user}')
        cursor = conn.cursor()
        return cursor
    
    def ConnectToDatabase(self, database, user, password, host, port):
        
        '''Connect to Database'''
        
        conn = psycopg2.connect(database = database, user=user,password=password,host=host,port=port)
        conn.autocommit = True
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        print(f'Successfully connected | User:{user}')
        cursor = conn.cursor()
        return cursor
    
    def constructDatabases(self):
        
        '''Create Databases'''
        
        print("Initializing Databases...")
        self.cursor.execute(self.Kill)
        
        for DB in self.DB_list:
            self.cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = \'{}\'".format(DB))
            exists = self.cursor.fetchone()
            
            if exists == None:
                # Create Database
                self.cursor.execute("CREATE DATABASE {}".format(DB))
                print("Database {} has been created!".format(DB))
            else:
                print("Database {} is already existed!".format(DB))
    
    def constructTables(self):
        
        '''Iterate through each database and create tables'''
        
        for DB in self.DB_detail.keys():
            temp_cursor = self.ConnectToDatabase(DB,self.user,self.password,self.host,self.port)
            for table in self.DB_detail[DB].keys():
                query = self.TableBuilder(DB, table)
                temp_cursor.execute(query)
                print("Table {} has been created in {}".format(table, DB))
            
    def TableBuilder(self, DB, table):
        
        '''Helper function of constructTable function'''
        
        query_head = '''CREATE TABLE {} '''.format(table)
        query_head += self.DB_detail[DB][table]
        #print(query_head)
        return query_head
            
            

            
            