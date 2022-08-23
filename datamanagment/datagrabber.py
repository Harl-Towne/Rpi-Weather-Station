import traceback
from typing import Tuple, Union

import pandas
import requests as req
import pandas as pd
import re
from time import sleep
import os
from colorama import Fore
from pandas import DataFrame, Timedelta
from pandas._libs import NaTType


def get_data(address="http://192.168.4.15") -> Tuple[DataFrame, Union[Timedelta, NaTType, NaTType]]:
    """
    Generic function for getting csv data over http. Returns the data formatted as pandas dataframe or None if an
    error was encountered.

    :rtype: pandas.DataFrame or None
    """
    try:
        # get data from weather station
        r = req.get(address, timeout=10)

        # error shit
        if r.status_code == 204:
            return None, None
        if r.status_code == 400:
            print(Fore.RED + "Error: 400, Bad Request")
            return None, None

        # get meta-data
        measurement_interval = pd.Timedelta("{}ms".format(r.headers["MeasurementInterval"]))
        start_epoch = int(r.headers["StartEpoch"])  # this is a negative number specifying how many epochs ago the data starts
        keys = re.split(",", re.sub(" ", "", r.headers["Feilds"]))
        # current datetime for later
        now = pd.Timestamp.now().floor(measurement_interval)

        # initialise dit
        data_dict = dict()
        data_dict["datetime"] = []
        for key in keys:
            data_dict[key] = list()

        # process data from request
        for row_num, line in enumerate(re.split("\n", r.text)):
            if line is None or line == "":
                continue
            datum = re.split(",", re.sub(" ", "", re.sub("[\r\n]", "", line)))
            data_dict["datetime"].append(now + (measurement_interval * (start_epoch + row_num + 1)))  # +1 so that it ends on 0
            for col_num, key in enumerate(keys):
                data_dict[key].append(datum[col_num])
                
        df = pd.DataFrame(data_dict)
        
        for key in keys:
            df[key] = pd.to_numeric(df[key])
        
        print("Successfully got data")
        return df, measurement_interval

    # more error shit
    except KeyboardInterrupt:
        raise KeyboardInterrupt
    except Exception as e:
        print("Error getting data from station:\n", e)
        return None, None


def test():
    """
    Test function that periodically gets and displays latest data.
    """
    while True:
        data = get_data()
        if data is not None:
            os.system("clear")
            print(data.iloc[-1, 1:])
        sleep(4)
