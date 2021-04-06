import requests
import json
from typing import List, Dict

from src.utils import UrlBundler, Storer, Dbcontext, Key
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
    #myStorage.import2Database("ProjectData")

    # get devices of every project.
    deviceMeta = myReq.getDevicesOfProject(myStorage)
    deviceMeta_processed = Parser.parseDevicesMeta(deviceMeta)
    myStorage.insert(deviceMeta_processed, "DeviceMeta")

    print(myStorage.storage["DeviceMeta"][0])
    # import data into database.
