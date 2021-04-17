# import essential modules
import requests
import sys
import json
from typing import List, Dict
import pandas as pd

# import main functionality
from src.dbcontext import Dbcontext, Storer
from src.utils import UrlBundler, Key
from src.requester import Requester
from src.parser import Parser


projects = {   
    '565':["rh", "pm1", "no", "amb_temp", "rainfall", "no2", "pm10", "o3", 
           "pm2_5", "co2", "so2", "wd_hr", "ws_hr",  "co", "nox", "nh3", "thc", 
           "nmhc", "uva", "pressure"],
    '624':["rh", "pm1", "no", "amb_temp", "rainfall", "no2", 
           "pm10", "o3", "co", "wind_direc", "wind_speed", "so2", 
           "pressure", "nox", "uva", "nmhc", "thc"],
    '891':["pm2_5", "temperature", "humidity"],
    '1156':["sfm_flow", "pm2_5_uart", "voc", "pm2_5_i2c", "temperature",
            "humidity", "speed", "lat", "lon"]
}

time_interval = {
       '565': "60",
       '624': "1",
       '891': "3",
       '1156': None
}