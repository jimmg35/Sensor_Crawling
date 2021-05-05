
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
                voc = Total_dataChunk[interval][projectid][0]
                pm25 = Total_dataChunk[interval][projectid][1]
                humidity = Total_dataChunk[interval][projectid][2]
                temperature = Total_dataChunk[interval][projectid][3]
                for device_voc, device_pm, device_hum, device_temp in zip(voc, pm25, humidity, temperature): # for each device
                    for v, p, h, t in zip(device_voc["etl"], device_pm["etl"], device_hum["etl"], device_temp["etl"]): # for every time
                        date = t["start"].split(' ')[0]
                        time = t["start"].split(' ')[1]
                        row_data = [device_pm["deviceId"], v["avg"], v["max"], v["min"], v["median"], 
                                                           p["avg"], p["max"], p["min"], p["median"],
                                                           h["avg"], h["max"], h["min"], h["median"],
                                                           t["avg"], t["max"], t["min"], t["median"], 
                                                           date.split("-")[0], date.split("-")[1], date.split("-")[2],
                                                           time.split(":")[0], time.split(":")[1], time.split(":")[2].split(".")[0],
                                                           t["start"]]
                        total.append(row_data)
                output_per_proj[projectid] = total
            output[str(interval)] = output_per_proj
        return output

    @staticmethod
    def parseTotalDataChunk_spacial(Total_dataChunk):
        """
            {
                528:[[rowdata_at_time],[],[]],
                527:[],
                .
                .
                .
            }
        """
        output = {}
        for projectid in list(Total_dataChunk.keys()):
            data_T = ParserTool.Transpose(Total_dataChunk[projectid])
            
            total = []
            for device_row in data_T: # for each device
                

                dataChunk = []
                for index, device in enumerate(device_row): # for each sensor of a device
                    dataChunk.append(device["etl"])
                dataChunk_T = ParserTool.Transpose(dataChunk)

                
                for row in dataChunk_T: # for same time and different sensor
                    temp = [device_row[0]["deviceId"]]
                    for index, sensor_at_time in enumerate(row):
                        temp += [sensor_at_time["avg"],
                                 sensor_at_time["max"],
                                 sensor_at_time["min"],
                                 sensor_at_time["median"]]
                        if index == (len(row)-1):
                            date = sensor_at_time["start"].split(' ')[0]
                            time = sensor_at_time["start"].split(' ')[1]
                            temp += [date.split("-")[0], date.split("-")[1], date.split("-")[2],
                                     time.split(":")[0], time.split(":")[1], time.split(":")[2].split(".")[0],
                                     t["start"]]
                    total.append(temp)
            output[projectid] = total
        return output

    @staticmethod
    def parseMinuteData(data_chunk, ts):
        
        """ 解析時間區段內 一個device各測項的資料 """

        # data = {"voc":[], "pm2_5":[], "humidity":[], "temperature":[]}
        # date = []
        # time = []
        # deviceid = []
        # for i in range(0, len(data_chunk)):
        #     data[data_chunk[i]["id"]].append(data_chunk[i]["value"][0])
        #     if i%4 == 0 and i != (len(data_chunk)-1):
        #         date.append(data_chunk[i]["createTime"].split(' ')[0]) 
        #         time.append(data_chunk[i]["createTime"].split(' ')[1].split(':'))
        #         deviceid.append(data_chunk[i]["deviceId"])
        # return deviceid, data, date, time
        
        data_s = []
        date = []
        time = []
        deviceid = []
        for i in range(0, len(data_chunk), 4):
            classify = {"voc":None, "pm2_5":None, "humidity":None, "temperature":None}
            for j in range(0, 4):
                classify[data_chunk[i+j]["id"]] = data_chunk[i+j]["value"][0]
            
            data_s.append(classify)
            date.append(data_chunk[i]["createTime"].split(' ')[0]) 
            time.append(data_chunk[i]["createTime"].split(' ')[1].split(':'))
            deviceid.append(data_chunk[i]["deviceId"])
        
        return data_s, date, time, deviceid
                        


                
                

            
                    
            
            

                
            







