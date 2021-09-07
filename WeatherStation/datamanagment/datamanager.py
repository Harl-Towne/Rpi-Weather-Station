import pandas as pd
import os


class Data:

    def __init__(self, storage_path="data",
                 real_time_duration=pd.Timedelta("24 hours"),
                 agg_durations=(pd.Timedelta("7 days"), pd.Timedelta("365 days")),
                 agg_intervals=(1800, 86400, 86400),
                 initial_data=None):
        self.real_time_duration = real_time_duration
        self.agg_durations = agg_durations
        self.agg_intervals = [pd.Timedelta("{}S".format(agg_interval)) for agg_interval in agg_intervals]
        self.data_path = os.path.join(os.getcwd(), storage_path)

        # if initial data was provided use it to create empty history arrays
        if initial_data is not None:
            # create real time dataframe
            self.rt_data = initial_data
            # initialise aggregated dataframes
            self.agg_data = list()

            # create empty dataframe because specifying columns in pd.DataFrame() doesn't work on raspberry pi
            empty_df = dict()
            for column in list(initial_data.columns):
                empty_df[column] = []
            # create aggregate dataframes
            for i in range(len(agg_durations)):
                self.agg_data.append(pd.DataFrame(empty_df))
            # create additional dataframe if it is required for the all-time dataframe
            if agg_intervals[-2] != agg_intervals[-1]:
                self.agg_data.append(pd.DataFrame(empty_df))
            return

        # if initial data was not provided try and load previously saved data data
        files = os.listdir(self.data_path)

        # load real time data
        if "rt_data" in files and os.path.isfile(os.path.join(self.data_path, "rt_data")):
            self.rt_data = pd.read_csv(os.path.join(self.data_path, "rt_data"))
        else:
            raise Exception("Previous data not found in {} and sample data was not supplied.".format(self.data_path))

        # load aggregated dataframes
        self.agg_data = list()
        for i in range(len(agg_durations)):
            fn = str(i)
            bfn = "{},bak".format(str(i))
            if bfn in files and os.path.isfile(os.path.join(self.data_path, bfn)):
                self.agg_data.append(pd.read_csv(os.path.join(self.data_path, bfn)))
            elif fn in files and os.path.isfile(os.path.join(self.data_path, fn)):
                self.agg_data.append(pd.read_csv(os.path.join(self.data_path, fn)))
            else:
                raise Exception("Previous data not found in {} and sample data was not supplied.".format(self.data_path))

        # load  additional dataframe if it is required for the all-time dataframe
        if agg_intervals[-2] != agg_intervals[-1]:
            i = len(self.agg_data)
            fn = str(i)
            bfn = "{},bak".format(str(i))
            if bfn in files and os.path.isfile(os.path.join(self.data_path, bfn)):
                self.agg_data.append(pd.read_csv(os.path.join(self.data_path, bfn)))
            elif fn in files and os.path.isfile(os.path.join(self.data_path, fn)):
                self.agg_data.append(pd.read_csv(os.path.join(self.data_path, fn)))
            else:
                raise Exception("Previous data not found in {} and sample data was not supplied.".format(self.data_path))

        # call conversion function
        self._convert_columns()

    def _convert_columns(self):
        return

    def update_data(self):
        pass

    def aggregate_data(self):
        pass

    def save_data(self):
        pass
