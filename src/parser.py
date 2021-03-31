
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
        
        device_att_union_proj = []
        att_union_proj = []
        for project in list(deviceMeta.keys()):
            
            for devices in deviceMeta[project]: # for different project key.
                for Adevice in devices["data"]: # for each device of a project key.
                    
                    # get union attribute of a device
                    ParserTool.findUnionField_obj(device_att_union_proj,
                                              Adevice)

                    #print(Adevice["id"], devices["ProjectKey"], project, Adevice["name"],
                    #    Adevice["type"], Adevice["lat"], Adevice["lon"], Adevice["alt"])
                    
                    for i in Adevice["attributes"]:
                        try:
                            if i["key"] not in att_union_proj:
                                att_union_proj.append(i["key"])
                        except:
                            print(project, i.keys())

            #     #print(project, device["id"], device["name"])

        print(str(project)+" A: " + str(len(device_att_union_proj)))
        print(str(project)+" B: " + str(len(att_union_proj)))


class ParserTool():
    """
        class hosts complex function for Parser 
    """

    @staticmethod
    def findUnionField_obj(union_arr, an_object):
        for i in list(an_object.keys()):
            if i not in union_arr:
                union_arr.append(i)
        