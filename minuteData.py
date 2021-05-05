# import essential modules
import requests
import sys
import json
from typing import List, Dict
import pandas as pd

# import main functionality
from src.dbcontext import Dbcontext, Storer
from src.utils import UrlBundler, Key
from src.requester import Requester
from src.parser import Parser


# projects = ['528','671','672','673','674','675',
#             '677','678','680','709','756','1024','1025',
#             '1027','1029','1032','1034','1035','1036',
#             '1048','1058','1071','1072','1075','1079',
#             '1084','1085','1102','1120','1145','1147',
#             '1162','1167','1184','1189','1192','1207']

projects = ['1024']

item  = ['voc', 'pm2_5', 'humidity', 'temperature']


class TimeStamper():
    def build(self, chunk):
        return chunk[0] + "-" + chunk[1] + "-" + chunk[2] + " " + chunk[3] + ":" + chunk[4] + ":" + chunk[5]
    
    def build_minute(self, chunk):
        return chunk[0] + "-" + chunk[1] + "-" + chunk[2] + " " + chunk[3] + ":" + chunk[4]

        
    def parse(self, stamp):
        date = stamp.split(' ')[0]
        time = stamp.split(' ')[1]
        year = date.split('-')[0]
        month = date.split('-')[1]
        day = date.split('-')[2]
        hour = time.split(":")[0]
        minute = time.split(":")[1]
        second = time.split(":")[2]
        return [year,month,day,hour,minute,second]
    
    def parse_minute(self, stamp):
        date = stamp.split(' ')[0]
        time = stamp.split(' ')[1]
        year = date.split('-')[0]
        month = date.split('-')[1]
        day = date.split('-')[2]
        hour = time.split(":")[0]
        minute = time.split(":")[1]
        return [year,month,day,hour,minute]



start_month = 1

if __name__ == "__main__":

    # initializer timer
    ts = TimeStamper()

    # initialize basic object.
    myKey = Key()
    myBundler = UrlBundler()
    myReq = Requester(myBundler, myKey)

    # initialize dbcontext
    myDBcontext = Dbcontext({"user":str(sys.argv[1]), 
                            "password":str(sys.argv[2]), 
                            "host":str(sys.argv[3]), 
                            "port":str(sys.argv[4])}, "sensordata")
    myStorage = Storer(myDBcontext)

    
    for project in projects[0:1]:
        data = myDBcontext.queryMinuteMetadata(project)
        for device in data: #[0:1]

            # build the time stamp
            start = ts.build(["2021", "01", "01", "00", "00", "00.000"])
            end = ts.build(["2021", "01", "31", "23", "59", "00.000"])
            compare = ts.build_minute(["2021", "01", "31", "23", "59"])
            
            # request for data of a device in a time interval
            data = myReq.getMinuteDataOfProject_interval_device(device[0], device[1], start, end, compare, ts)
            if data == None: # if request failed
                continue
            else: # if request seccess
                data_s, date, time, deviceid = Parser.parseMinuteData(data, ts)
                myDBcontext.ImportMinuteData(deviceid, data_s, date, time, project, start_month)
                print("-- {} import complete".format(device))
        print("--- {} project complete".format(project))
        print("=======================================")



