import sys

import numpy as np
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMainWindow, QGridLayout

import main_ui

import pyqtgraph as pg

from datamanagment.datagrabber import get_data
from datamanagment.weatherdatamanager import WeatherData


class mainWeatherWindow(QMainWindow, main_ui.Ui_MainWindow):
    wind_directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]

    def __init__(self):
        print("#"*20)
        super().__init__()
        self.setupUi()

    def setupUi(self, **kwargs):
        super(mainWeatherWindow, self).setupUi(self)

        # get data
        try:
            print("###### trying to load data from disk ######")
            self.data = WeatherData()
        except KeyboardInterrupt:
            raise KeyboardInterrupt
        except:
            print("failed")
            print("###### trying to get data from station instead ######")
            try:
                init_data = get_data()
                self.data = WeatherData(initial_data=init_data)
            except KeyboardInterrupt:
                raise KeyboardInterrupt
            except:
                print("failed")
                sys.exit(-1)
            finally:
                print("succeeded")
        finally:
            print("succeeded")

        # data update timer
        self.newdata_timer = QTimer()
        self.newdata_timer.timeout.connect(self.data.update_data)
        self.newdata_timer.start(1000*5)

        # data save timer
        self.savedata_timer = QTimer()
        self.savedata_timer.timeout.connect(self.data.save_data)
        self.savedata_timer.start(1000*60*1)

        # data aggregate timer
        self.aggdata_timer = QTimer()
        self.aggdata_timer.timeout.connect(self.data.aggregate_data)
        self.aggdata_timer.start(int(1000 * self.data.agg_intervals[0].total_seconds() * 1.5))

        # set starting screen
        self.stackedWidget.setCurrentIndex(0)

        # connect all toolbar buttons to actions
        self.actionDashboard.triggered.connect(lambda: self.toolbar_clicked(0))
        self.actionDaily_Graphs.triggered.connect(lambda: self.toolbar_clicked(1))
        self.actionWeekly_Graphs.triggered.connect(lambda: self.toolbar_clicked(2))
        self.actionYearly_Graphs.triggered.connect(lambda: self.toolbar_clicked(3))
        self.actionAll_Time_Graphs.triggered.connect(lambda: self.toolbar_clicked(4))
        self.actionSettings.triggered.connect(lambda: self.toolbar_clicked(5))
        self.actionExit.triggered.connect(lambda: sys.exit())

        # update timers
        self.dashboard_timer = QTimer()
        self.dashboard_timer.timeout.connect(self.update_dashboard)
        self.dashboard_timer.start(1000 * 5)

        self.daily_timer = QTimer()
        self.daily_timer.timeout.connect(self.update_daily)
        self.daily_timer.start(1000 * 5)

        self.weekly_timer = QTimer()
        self.weekly_timer.timeout.connect(self.update_weekly)
        self.weekly_timer.start(1000 * 60 * 5)

        self.yearly_timer = QTimer()
        self.yearly_timer.timeout.connect(self.update_yearly)
        self.yearly_timer.start(1000 * 60 * 60 * 1)

        self.all_timer = QTimer()
        self.all_timer.timeout.connect(self.update_all)
        self.all_timer.start(1000 * 60 * 60 * 1)

        # create curves for all the plots
        self.plotcurves = {"daily": {}, "weekly": {}, "yearly": {}, "all": {}}

        self.plotcurves["daily"]['temp'] = self.tempDailyGraph.plot(np.array([0]))
        self.plotcurves["daily"]['hum'] = self.humDailyGraph.plot(np.array([0]))
        self.plotcurves["daily"]['wind'] = self.windDailyGraph.plot(np.array([0]))
        self.plotcurves["daily"]['rain'] = self.rainDailyGraph.plot(np.array([0]))

    def toolbar_clicked(self, btn_no):
        self.stackedWidget.setCurrentIndex(btn_no)

    def update_dashboard(self):
        latest_data = self.data.rt_data.iloc[-1, :]
        self.currentTempFeild.setText(str(latest_data["temperature"]))
        self.currenthumFeild.setText(str(latest_data["humidity"]))
        self.windSpeedFeild.setText(str(latest_data["wind_speed"]))
        self.windDirectFeild.setText(self.wind_directions[int(latest_data["wind_direction"])])
        self.dayRainFeild.setText(str(latest_data["rain"]))

    def update_daily(self):
        self.plotcurves["daily"]["temp"].setData(np.array(self.data.rt_data.loc[:, "temperature"].to_numpy(), dtype=float))
        self.plotcurves["daily"]["hum"].setData(np.array(self.data.rt_data.loc[:, "humidity"].to_numpy(), dtype=float))
        self.plotcurves["daily"]["wind"].setData(np.array(self.data.rt_data.loc[:, "wind_speed"].to_numpy(), dtype=float))
        self.plotcurves["daily"]["rain"].setData(np.array(self.data.rt_data.loc[:, "rain"].to_numpy(), dtype=float))

    def update_weekly(self):
        pass

    def update_yearly(self):
        pass

    def update_all(self):
        pass
