# import essential modules
import requests
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
sensor_item = ['pm2_5', 'humidity', 'temperature']
time_interval = [1, 60]

start = "2021-01-01 00:00:00" 
end = "2021-01-31 00:00:00"





if __name__ == "__main__":

    # initialize basic object.
    myKey = Key()
    myBundler = UrlBundler()
    myReq = Requester(myBundler, myKey)

    # initialize dbcontext
    myDBcontext = Dbcontext({"user":"postgres",
                                "password":"jim60308",
                                "host":"localhost",
                                "port":"5432"}, "sensordata")
    myStorage = Storer(myDBcontext)


    # query from database
    rawdata = myDBcontext.queryDeviceSensorMeta_fixed()
    # transform into pandas dataframe
    DeviceSensorMeta = Parser.transformDeviceSensorMeta(rawdata)
    

    Total_dataChunk = {}
    for interval in time_interval: #[1:2]
        project_dataChunk = {}
        for projectid in projects: #[0:1]
            returnData = myReq.getIntervalDataOfSensor(DeviceSensorMeta, 
                                                       sensor_item, projectid, interval, start, end)
            project_dataChunk[projectid] = returnData
            print("{} has complete.".format(projectid))
        Total_dataChunk[str(interval)] = project_dataChunk

    Total_dataChunk_processed = Parser.parseTotalDataChunk(Total_dataChunk)


