
# Author : @jimmg35


import requests
import json
from typing import List, Dict
from .utils import UrlBundler, Key



class Requester():
    """
        Requester for handling common task
    """
    def __init__(self, UB: UrlBundler, key: Key) -> None:
        self.UB: UrlBundler = UB
        self.Key: Key = key
    
    def getAllProjectsMeta(self) -> List[Dict]:
        ''' 
            Request for all project key 
        '''

        response = requests.request("GET", 
                                    self.UB.getProjects, 
                                    headers={"CK":self.Key.key})
        print("All Projects Meta downloaded!")
        return json.loads(response.text)


    def getDevicesOfProject(self, MyStorage, chooseOneKey=True):
        ''' 
            Request for every device of all project 
        '''

        output = {}
        for i in list(MyStorage.storage["ProjectData"].keys()): #[0:10]
            data_per_proj = []
            keys = MyStorage.storage["ProjectData"][i]["keys"]
            # Choose only one Project Key to request.
            if chooseOneKey:
                response = requests.request("GET",
                                            self.UB.getDevicesOfProj,
                                            headers={"CK":keys[0]})
                data = json.loads(response.text)
                data_per_proj.append({"data":data, "ProjectKey":keys[0]})
                output[str(i)] = data_per_proj
                print("Project[{}] devices data downloaded!".format(i))
            else:
                for j in keys:
                    response = requests.request("GET",
                                                self.UB.getDevicesOfProj,
                                                headers={"CK":j})
                    data = json.loads(response.text)
                    data_per_proj.append({"data": data, "ProjectKey":j})
                output[str(i)] = data_per_proj
                print("Project[{}] devices data downloaded!".format(i))
        return output


    def getSensorsOfDevice(self, MyStorage):
        '''
            Request for sensor meta of all device
        '''
        output = {}
        for device in MyStorage.storage["DeviceMeta"]:
            #device["ProjectID"]
            headers = {'CK': device["ProjectKey"]}
            response = requests.request("GET", 
                                        self.UB.getSensorOfDev.format(device["id"]), 
                                        headers=headers)
            data = [json.loads(response.text), device["ProjectKey"]]
            output[str(device["id"])] = data
            print("{} downloaded!!".format(device["id"]))
        return output