
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


    def getIntervalDataOfSensor(self, DeviceSensorMeta, sensor_item, projectid, interval, start, end):
        """
            get interval sensor data for one project
              pm                         hum  temp
             [[{device1},{device2},...], [],  []]
        """
        project_data = DeviceSensorMeta[DeviceSensorMeta["projectid"] == projectid]
        each_sensor_device_data = []
        for sensorid in sensor_item: # pm2.5, humidity, temperature
            each_device_data = []
            count = 0  # control how many devices per project
            for row in project_data.iterrows():
                response = requests.request("GET", 
                                            self.UB.getIntervalData.format(row[1]["deviceid"], sensorid, 
                                                     start, end, interval), 
                                            headers={'CK': row[1]["projectkey"]})
                each_device_data.append(json.loads(response.text))
                print("intervar: {} project_id:{} device_id: {}, sensor_id: {}".format(str(interval),
                                                                                       projectid, 
                                                                                       row[1]["deviceid"], 
                                                                                       sensorid))
                count += 1
                if count == 2:
                    break
            each_sensor_device_data.append(each_device_data)
        return each_sensor_device_data