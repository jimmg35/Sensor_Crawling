
# Author : @jimmg35

import requests
import json
from typing import List, Dict
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
        output = {}
        for i in projMeta:
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
        att_union_proj.remove('')
        
        # column set goes into database
        total_column = device_att_union_proj + att_union_proj
        total_column.remove("attributes")
        ParserTool.addTag2DubField(total_column)


        # Extracting value of device (lots of exception)
        all_device_data = []
        for project in list(deviceMeta.keys()):
            for devices in deviceMeta[project]: # for different project key.
                device_chunk = {}
                for Adevice in devices["data"]:
                    device_chunk["ProjectKey"] = devices["ProjectKey"]
                    device_chunk["ProjectID"] = project
                    ParserTool.takeValueOfAtt(device_chunk, Adevice, device_att_union_proj)
                    ParserTool.takeValueOfAttChunk(device_chunk, Adevice, att_union_proj)
                all_device_data.append(device_chunk)
        return all_device_data

        
        





