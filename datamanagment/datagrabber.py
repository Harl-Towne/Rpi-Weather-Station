import traceback
import pandas
import requests as req
import pandas as pd
import re
from time import sleep
import os
from colorama import Fore


def get_data(address="http://192.168.4.15") -> pandas.DataFrame:
    """
    Generic function for getting csv data over http. Returns the data formatted as pandas dataframe or None if an
    error was encountered.

    :rtype: pandas.DataFrame or None
    """
    try:
        # current datetime for later
        now = pd.Timestamp.now()

        # get data from weather station
        r = req.get(address, timeout=10)

        # error shit
        if r.status_code == 204:
            return None
        if r.status_code == 400:
            print(Fore.RED + "Error: 400, Bad Request")
            return None

        # get meta-data
        interval = pd.Timedelta("{}ms".format(r.headers["MeasurementInterval"]))
        start_epoch = int(r.headers["StartEpoch"])
        keys = re.split(",", re.sub(" ", "", r.headers["Feilds"]))

        # initialise dit
        data_dict = dict()
        data_dict["datetime"] = []
        for key in keys:
            data_dict[key] = list()

        # process data from request
        print("now:", now)
        print("int:", interval)
        print("start:", start_epoch)
        print("-"*20)
        for row_num, line in enumerate(re.split("\n", r.text)):
            if line is None or line == "":
                continue
            datum = re.split(",", re.sub(" ", "", re.sub("[\r\n]", "", line)))
            data_dict["datetime"].append(now + (interval * (start_epoch + row_num)))
            print(now + (interval * (start_epoch + row_num)))
            for col_num, key in enumerate(keys):
                data_dict[key].append(datum[col_num])

        print("Successfully got data")
        return pd.DataFrame(data_dict)

    # more error shit
    except KeyboardInterrupt:
        raise KeyboardInterrupt
    except Exception as e:
        print("Error getting data from station:\n", e)
        # traceback.print_exc()
        return None


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
