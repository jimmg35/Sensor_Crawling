import requests
import json
from typing import List, Dict

from src.utils import UrlBundler, Storer, Key
from src.requester import Requester
from src.parser import Parser




if __name__ == "__main__":

    # initialize basic object
    myKey = Key()
    myBundler = UrlBundler()
    myStorage = Storer()

    # initialize my requester
    myReq = Requester(myBundler, myKey)

    # get projects metadata
    projMeta = myReq.getAllProjectsMeta()
    projMeta_processed = Parser.parseProjectMeta(projMeta)
    myStorage.insert(projMeta_processed, "ProjectData")

    #print(myStorage.storage["ProjectData"])

    # get devices of every project
    deviceMeta = myReq.getDevicesOfProject(myStorage)
    Parser.parseDevicesMeta(deviceMeta)