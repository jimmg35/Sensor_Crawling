
# Author : @jimmg35

import requests
import json
from typing import List, Dict
import pandas as pd 
from .parser_engine import ParserTool

class Parser():
    """
        Parser for parsing the content derived from Requester
    """

    @staticmethod
    def parseProjectMeta(projMeta: List[Dict]) -> Dict:
        """
            {"id":{"name": name, "keys": keys}}
        """

        queryset = ['528','671','672','673','674',
                    '675','677','678','680','709',
                    '756','1024','1025','1027','1029',
                    '1032','1034','1035','1036','1048',
                    '1058','1071','1072','1075','1079',
                    '1084','1085','1102','1120','1145',
                    '1147','1162','1167','1184','1189',
                    '1192','1207','1156','565','624','891']
        output = {}
        for i in projMeta:
            if str(i["id"]) in queryset:
                keys = [k["key"] for k in i["projectKeys"]]
                output[str(i["id"])] = {"name":i["name"], "keys":keys}
        return output

    @staticmethod  # project 956 and 1019 doesn't have attribute.
    def parseDevicesMeta(deviceMeta: List[Dict]) -> Dict:
        """
            [{column1: value, column2: value}, ... ]
        """
        # Union every field of each device.
        device_att_union_proj = []
        att_union_proj = []
        for project in list(deviceMeta.keys()):
            for devices in deviceMeta[project]: # for different project key.
                for Adevice in devices["data"]: # for each device of a project key.
                    # get union attribute of a device
                    ParserTool.findUnionField_obj(device_att_union_proj, Adevice)
                    ParserTool.findUnionField_att(att_union_proj, Adevice["attributes"])
        #att_union_proj.remove('')

        # Extracting value of device (lots of exception)
        all_device_data = []
        for project in list(deviceMeta.keys()):
            for devices in deviceMeta[project]: # for different project key.
                for Adevice in devices["data"]:
                    device_chunk = {}
                    device_chunk["ProjectKey"] = devices["ProjectKey"]
                    device_chunk["ProjectID"] = project
                    ParserTool.takeValueOfAtt(device_chunk, Adevice, device_att_union_proj)
                    ParserTool.takeValueOfAttChunk(device_chunk, Adevice, att_union_proj, device_att_union_proj)
                    all_device_data.append(device_chunk)
        return all_device_data

    @staticmethod
    def parseSensorMeta(sensorMeta: List[Dict]):
        """
            [ [deviceid, projectkey, [sensor1...]] , [], ...]
        """
        output = []
        for deviceId in list(sensorMeta.keys()):
            sensor_item = []
            temp = [deviceId, sensorMeta[deviceId][1]]
            for item in sensorMeta[deviceId][0]:
                sensor_item.append(item["id"])
            temp.append(sensor_item)
            output.append(temp)
        return output
    
    @staticmethod
    def transformDeviceSensorMeta(DeviceSensorMeta):
        """
            pandas dataframe
        """
        total = []
        for i in DeviceSensorMeta:
            total.append([str(i[0]), i[1], i[2]])
        return pd.DataFrame(total, columns=["projectid", "projectkey", "deviceid"])

    @staticmethod
    def parseTotalDataChunk(Total_dataChunk):
        """
            {
                1:{
                    528:[[rowdata_at_time],[],[]],
                    527:[],
                    .
                    .
                    .
                },
                60:{
                    528:[],
                    527:[],
                    .
                    .
                    .
                }
            }
        """
        output = {}
        for interval in list(Total_dataChunk.keys()): # 1 or 60 mins
            output_per_proj = {}
            for projectid in list(Total_dataChunk[interval].keys()): # for each project
                total = []
                pm25 = Total_dataChunk[interval][projectid][0]
                humidity = Total_dataChunk[interval][projectid][1]
                temperature = Total_dataChunk[interval][projectid][2]
                for device_pm, device_hum, device_temp in zip(pm25, humidity, temperature): # for each device
                    for p, h, t in zip(device_pm["etl"], device_hum["etl"], device_temp["etl"]): # for every time
                        date = t["start"].split(' ')[0]
                        time = t["start"].split(' ')[1]
                        row_data = [device_pm["deviceId"], p["avg"], p["max"], p["min"], p["median"],
                                                           h["avg"], h["max"], h["min"], h["median"],
                                                           t["avg"], t["max"], t["min"], t["median"], 
                                                           date.split("-")[0], date.split("-")[1], date.split("-")[2],
                                                           time.split(":")[0], time.split(":")[1], time.split(":")[2].split(".")[0], 
                                                           time]
                        total.append(row_data)
                output_per_proj[projectid] = total
            output[str(interval)] = output_per_proj
        return output








