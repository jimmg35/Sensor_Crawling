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


projects_item = {   
    '565':["rh", "pm1", "no", "amb_temp", "rainfall", "no2", "pm10", "o3", 
           "pm2_5", "co2", "so2", "wd_hr", "ws_hr",  "co", "nox", "nh3", "thc", 
           "nmhc", "uva", "pressure"],
    '624':["rh", "pm1", "no", "amb_temp", "rainfall", "no2", 
           "pm10", "o3", "co", "wind_direc", "wind_speed", "so2", 
           "pressure", "nox", "uva", "nmhc", "thc"],
    '891':["pm2_5", "temperature", "humidity"],
}


time_interval = {
    '891': "3",
    '565': "60",
    '624': "1",
    
}

#start = str(sys.argv[5]) + "-" + str(sys.argv[6]) + "-" + str(sys.argv[7]) + " 00:00:00" 
#end = str(sys.argv[8]) + "-" + str(sys.argv[9]) + "-" + str(sys.argv[10]) + " 00:00:00"
start = "2021-01-01 00:00:00"
end = "2021-01-02 00:00:00"


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
    rawdata = myDBcontext.queryDeviceSensorMeta_spacial()
    # transform into pandas dataframe
    DeviceSensorMeta = Parser.transformDeviceSensorMeta(rawdata)


    project_dataChunk = {}
    for projectid in list(time_interval.keys()):
        interval = time_interval[projectid]
        returnData = myReq.getIntervalDataOfSensor(DeviceSensorMeta,
                                                   projects_item[projectid], projectid, interval, start, end)
        project_dataChunk[projectid] = returnData
    

    project_dataChunk_processed = Parser.parseTotalDataChunk_spacial(project_dataChunk)
    print(project_dataChunk_processed)