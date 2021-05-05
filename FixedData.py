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


projects = ['528','671','672','673','674','675',
            '677','678','680','709','756','1024','1025',
            '1027','1029','1032','1034','1035','1036',
            '1048','1058','1071','1072','1075','1079',
            '1084','1085','1102','1120','1145','1147',
            '1162','1167','1184','1189','1192','1207']
sensor_item = ['voc', 'pm2_5', 'humidity', 'temperature']
time_interval = [60]

start = str(sys.argv[5]) + "-" + str(sys.argv[6]) + "-" + str(sys.argv[7]) + " 00:00:00" 
end = str(sys.argv[8]) + "-" + str(sys.argv[9]) + "-" + str(sys.argv[10]) + " 00:00:00"


if __name__ == "__main__":

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


    # query metadata from database
    rawdata = myDBcontext.queryDeviceSensorMeta_fixed()
    # transform into pandas dataframe
    DeviceSensorMeta = Parser.transformDeviceSensorMeta(rawdata)
    
    # requesting for history sensor data.
    Total_dataChunk = {}
    for interval in time_interval: #[1:2]
        project_dataChunk = {}
        for projectid in projects: # control how many project to be requested
            returnData = myReq.getIntervalDataOfSensor(DeviceSensorMeta, 
                                                       sensor_item, projectid, interval, start, end)
            project_dataChunk[projectid] = returnData
            print("{} has complete. interval: {}\n".format(projectid, interval))
        Total_dataChunk[str(interval)] = project_dataChunk

    # import data into database
    Total_dataChunk_processed = Parser.parseTotalDataChunk(Total_dataChunk)
    myStorage.insert(Total_dataChunk_processed, "FixedData")
    myStorage.import2Database("FixedData", sys.argv[5], sys.argv[6], sys.argv[9])



