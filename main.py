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
    myDBcontext = Dbcontext()
    myStorage = Storer(myDBcontext)

    # initialize my requester.
    myReq = Requester(myBundler, myKey)

    # get projects metadata.
    projMeta = myReq.getAllProjectsMeta()
    projMeta_processed = Parser.parseProjectMeta(projMeta)
    myStorage.insert(projMeta_processed, "ProjectData")

    # get devices of every project.
    # deviceMeta = myReq.getDevicesOfProject(myStorage)
    # deviceMeta_processed = Parser.parseDevicesMeta(deviceMeta)
    # myStorage.insert(deviceMeta_processed, "DeviceMeta")

    # import data into database.
