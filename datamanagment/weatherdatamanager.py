import math

import numpy as np
import pandas as pd
from datamanagment import datamanager
from datamanagment import datagrabber
from threadqueue import threadqueuing
from super_awsome_helper_functions import recursive_mkdir, safe_save_dataframe


# TODO: delete data somewhere
class WeatherData(datamanager.Data):

    def _convert_columns(self):
        # convert rt_data
        for column in self.rt_data.columns:
            if column == "datetime":
                self.rt_data[column] = pd.to_datetime(self.rt_data[column])
            else:
                self.rt_data[column] = pd.to_numeric(self.rt_data[column])

        # convert aggregated data
        for i in range(len(self.agg_data)):
            for column in self.agg_data[i].columns:
                if column == "datetime":
                    self.agg_data[i][column] = pd.to_datetime(self.agg_data[i][column])
                else:
                    self.agg_data[i][column] = pd.to_numeric(self.agg_data[i][column])

    @threadqueuing
    def aggregate_data(self):
        # for each aggregated dataset
        for i in range(len(self.agg_data)):
            print("########### {} ###########".format(i))
            # if the data is being aggregated from the real time data it needs to be done slightly differently
            if i == 0:
                source_data = self.rt_data
                initial_aggregation = True
            else:
                source_data = self.agg_data[i - 1]
                initial_aggregation = False

            if source_data.empty:
                print("no data to agg from")
                continue

            # get period and interval to aggregate data with
            interval = pd.Timedelta(self.agg_intervals[i])
            last_epoch = source_data.iloc[-1, :]["datetime"].round(interval)  # exclusive
            if self.agg_data[i].empty:
                first_epoch = source_data.iloc[0, :]["datetime"].round(interval)  # inclusive
            else:
                first_epoch = self.agg_data[0].iloc[-1, :]["datetime"] + interval  # inclusive

            print(first_epoch, last_epoch, "(", interval, ")")

            # aggregate data
            new_data = self._get_aggregated_data(first_epoch, last_epoch, interval, source_data, initial_aggregation)
            if new_data is None:
                print('no new')
                continue

            # if there was previous data: append. otherwise, just set as it avoids some conflicts
            if self.agg_data[i].empty:
                self.agg_data[i] = new_data
            else:
                self.agg_data[i] = pd.concat([self.agg_data[i], new_data], ignore_index=True)

            print(self.agg_data[i])

    @staticmethod
    def _get_aggregated_data(first_epoch, last_epoch, interval, source_data, initial_aggregation=False):
        aggregate_datums = list()
        # step through each epoch
        current_epoch = first_epoch
        last_used_index = 0
        while current_epoch < last_epoch:
            print(current_epoch)
            data_start = None  # inclusive
            data_end = None  # exclusive
            # get range of source data for dest datum
            for i in range(last_used_index, len(source_data)):  # this is the first point to try and optimise <=======#
                epoch = source_data.iloc[i, :]["datetime"].round(interval)
                if epoch == current_epoch and data_start is None:
                    data_start = i
                if epoch > current_epoch:
                    data_end = i
                    break

            # aggregate data into single datum
            agg_datum = dict()
            agg_datum["datetime"] = current_epoch
            if data_start is None and data_end is not None:
                # no data matching timeframe (insert null datum)
                # aggregate data into single datum
                for column in source_data.columns:
                    if column == "rain":
                        agg_datum[column] = [math.nan]
                    elif column == "wind_direction":
                        agg_datum[column] = [math.nan]
                    else:
                        if initial_aggregation:
                            agg_datum["max_{}".format(column)] = [math.nan]
                            agg_datum["min_{}".format(column)] = [math.nan]
                            agg_datum["avg_{}".format(column)] = [math.nan]
                        else:
                            agg_datum[column] = [math.nan]

            elif data_end is None:
                # reached end of df before current epoch was up - should not happen because of last_epoch variable
                raise Exception("This error should never be raised. ")
            else:
                ranged_data = source_data.iloc[data_start:data_end, 1:]
                print(ranged_data)
                print(ranged_data.dtypes)
                for column in ranged_data.columns:
                    if column == "rain":
                        agg_datum[column] = [ranged_data[column].sum()]
                    elif column == "wind_direction":
                        agg_datum[column] = [ranged_data[column].mode()[0]]
                    else:
                        if initial_aggregation:
                            print(column)
                            agg_datum["max_{}".format(column)] = [ranged_data[column].max()]
                            agg_datum["min_{}".format(column)] = [ranged_data[column].min()]
                            agg_datum["avg_{}".format(column)] = [ranged_data[column].mean()]
                        else:
                            if "max_" in column:
                                agg_datum[column] = [ranged_data[column].max()]
                            elif "min_" in column:
                                agg_datum[column] = [ranged_data[column].min()]
                            elif "avg_" in column:
                                agg_datum[column] = [ranged_data[column].mean()]
                            else:
                                raise Exception("Couldn't correctly re-aggregate data")

            aggregate_datums.append(pd.DataFrame(agg_datum))

            last_used_index = data_end
            current_epoch += interval
        print(aggregate_datums)
        print("-"*10)
        if len(aggregate_datums) == 0:
            return None
        return pd.concat(aggregate_datums, ignore_index=True)

    @threadqueuing
    def update_data(self):
        new_data, measurement_interval = datagrabber.get_data()
        if new_data is not None:
            last_recorded_time = self.rt_data.iloc[-1, :]["datetime"]
            first_new_time = new_data.iloc[0, :]["datetime"]
            print(new_data)
            print("="*20)
            print(first_new_time, last_recorded_time, first_new_time - last_recorded_time)
            if first_new_time - last_recorded_time > measurement_interval:
                print("hey there's a gap")
                nan_dict = dict()
                for key in new_data.columns:
                    nan_dict[key] = list()
                current_time = last_recorded_time + measurement_interval
                while current_time < first_new_time:
                    for key in new_data.columns:
                        nan_dict[key].append(np.NaN)
                    nan_dict['datatime'][-1] = current_time
                    current_time = current_time + measurement_interval
                nan_dataframe = pd.DataFrame(nan_dict)
                print(nan_dataframe)

            self.rt_data = pd.concat([self.rt_data, new_data], ignore_index=True)
        else:
            # raise Exception("Failed to update data")
            print("Failed to update data")

        print("#"*30)

    @threadqueuing
    def save_data(self):
        # make sure the folder to save files into exists
        recursive_mkdir(self.data_path)

        # save real time data
        safe_save_dataframe(self.rt_data, "rt_data", self.data_path)

        # save all aggregated data
        for i, agg_datum in enumerate(self.agg_data):
            if not agg_datum.empty:
                safe_save_dataframe(agg_datum, str(i), self.data_path)
