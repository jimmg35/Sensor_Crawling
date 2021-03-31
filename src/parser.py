
# Author : @jimmg35

import requests
import json
from typing import List, Dict

class Parser():
    """
        Parser for parsing the content derived from Requester
    """

    @staticmethod
    def parseProjectMeta(projMeta: List[Dict]) -> Dict:
        """
            {"id":{"name": name, "keys": keys}}
        """
        output = {}
        for i in projMeta:
            keys = [k["key"] for k in i["projectKeys"]]
            output[str(i["id"])] = {"name":i["name"], "keys":keys}
        return output

    @staticmethod  # project 956 and 1019 doesn't have attribute.
    def parseDevicesMeta(deviceMeta: List[Dict]) -> Dict:

        # Union every field of each device.
        device_att_union_proj = []
        att_union_proj = []
        for project in list(deviceMeta.keys()):
            for devices in deviceMeta[project]: # for different project key.
                for Adevice in devices["data"]: # for each device of a project key.
                    # get union attribute of a device
                    ParserTool.findUnionField_obj(device_att_union_proj, Adevice)
                    ParserTool.findUnionField_att(att_union_proj, Adevice["attributes"])

        
        # Extracting value of device (lots of exception)
        for project in list(deviceMeta.keys()):
            for devices in deviceMeta[project]: # for different project key.
                device_chunk = {}
                for Adevice in devices["data"]:
                    ParserTool.takeValueOfAtt(device_chunk, Adevice, device_att_union_proj)
                    ParserTool.takeValueOfAttChunk(device_chunk, Adevice, att_union_proj)
                    print(devices["ProjectKey"], project)


        total_column = device_att_union_proj + att_union_proj
        total_column.remove('')
        # column name that goes into database!
        ParserTool.addTag2DubField(total_column)





class ParserTool():
    """
        class hosts complex function for Parser 
    """

    @staticmethod
    def findUnionField_obj(union_arr, an_object):
        """ union all device meta field """
        for i in list(an_object.keys()):
            if i not in union_arr:
                union_arr.append(i)
    
    @staticmethod
    def findUnionField_att(union_arr, list_of_obj):
        """ union all device attribute field"""
        for i in list_of_obj:
            try:
                if i["key"] not in union_arr:
                    union_arr.append(i["key"])
            except:
                pass 

    @staticmethod
    def addTag2DubField(arr):
        unique = []
        for i in arr:
            if i not in unique:
                unique.append(i)

        for i in unique:
            count = 0
            for j in arr:
                if i == j:
                    count += 1
            if count != 1: # if field dub!
                arr[arr.index(i, arr.index(i)+1)] += "_DUB"

    @staticmethod
    def takeValueOfAtt(device_chunk, Adevice, union_colum):
        for i in union_colum:
            try:
                device_chunk[i] = Adevice[i]
            except:
                device_chunk[i] = None

    @staticmethod
    def takeValueOfAttChunk(device_chunk, Adevice, union_colum):
        for i in union_colum:
            value, status = ParserTool.checkFieldExistInAttribute(Adevice["attributes"], i)
            if status:
                device_chunk[i] = value
            else:
                device_chunk[i] = None

    @staticmethod
    def checkFieldExistInAttribute(att_chunk, att):
        flag = False
        att_index = 0
        for index, i in att_chunk:
            if att == i["key"]:
                flag = True
                att_index = index

        if flag:
            return att_chunk[att_index]["value"], flag
        else:
            return False
        