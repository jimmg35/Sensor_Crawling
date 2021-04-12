# import essential modules
import requests
import json
from typing import List, Dict

# import main functionality
from src.dbcontext import Dbcontext, Storer
from src.utils import UrlBundler, Key
from src.requester import Requester
from src.parser import Parser




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



    # get projects metadata.
    projMeta = myReq.getAllProjectsMeta()
    projMeta_processed = Parser.parseProjectMeta(projMeta)
    myStorage.insert(projMeta_processed, "ProjectData")

    # get devices of every project.
    deviceMeta = myReq.getDevicesOfProject(myStorage)
    deviceMeta_processed = Parser.parseDevicesMeta(deviceMeta)
    myStorage.insert(deviceMeta_processed, "DeviceMeta")

    # get sensors of every device.
    sensorMeta = myReq.getSensorsOfDevice(myStorage)
    sensorMeta_processed = Parser.parseSensorMeta(sensorMeta)
    myStorage.insert(sensorMeta_processed, "SensorMeta")
    


    # Import data into database.
    # myStorage.import2Database("ProjectData")
    # myStorage.import2Database("DeviceMeta")
    # myDBcontext.launchPatch()
    myStorage.import2Database("SensorMeta")