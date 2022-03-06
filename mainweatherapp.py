import sys

import numpy as np
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMainWindow, QGridLayout

import main_ui

import pyqtgraph as pg
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from datamanagment.datagrabber import get_data
from datamanagment.weatherdatamanager import WeatherData
from time import sleep


class mainWeatherWindow(QMainWindow, main_ui.Ui_MainWindow):
    wind_directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]

    def __init__(self):
        print("#"*20)
        super().__init__()
        self.setupUi()

    def setupUi(self, **kwargs):
        super(mainWeatherWindow, self).setupUi(self)

        daily_graph_layout = self.Daily_Graphs.layout()

        f1 = Figure()
        f2 = Figure()
        f3 = Figure()
        f4 = Figure()

        self.tempDailyGraph = FigureCanvas(f1)
        self.humDailyGraph = FigureCanvas(f2)
        self.windDailyGraph = FigureCanvas(f3)
        self.rainDailyGraph = FigureCanvas(f4)

        self.plotcurves["daily"]['temp'] = f1.add_subplot(111)
        self.plotcurves["daily"]['hum'] = f2.add_subplot(111)
        self.plotcurves["daily"]['wind'] = f3.add_subplot(111)
        self.plotcurves["daily"]['rain'] = f4.add_subplot(111)

        # self.tempDailyGraph.setObjectName("tempDailyGraph")
        # self.humDailyGraph.setObjectName("humDailyGraph")
        # self.windDailyGraph.setObjectName("windDailyGraph")
        # self.rainDailyGraph.setObjectName("rainDailyGraph")
        daily_graph_layout.addWidget(self.tempDailyGraph, 0, 0, 1, 1)
        daily_graph_layout.addWidget(self.humDailyGraph, 0, 1, 1, 1)
        daily_graph_layout.addWidget(self.windDailyGraph, 1, 0, 1, 1)
        daily_graph_layout.addWidget(self.rainDailyGraph, 1, 1, 1, 1)

        # get data
        try:
            print("###### trying to load data from disk ######")
            self.data = WeatherData()
            print("succeeded")
        except KeyboardInterrupt:
            raise KeyboardInterrupt
        except:
            print("failed")
            while True:
                print("###### trying to get data from station ######")
                try:
                    init_data, _ = get_data()
                    self.data = WeatherData(initial_data=init_data)
                    print("succeeded")
                    break
                except KeyboardInterrupt:
                    raise KeyboardInterrupt
                except:
                    print("failed")
                    sleep(3)

        # data update timer
        self.newdata_timer = QTimer()
        self.newdata_timer.timeout.connect(self.data.update_data)
        self.newdata_timer.start(1000*4)

        # data save timer
        self.savedata_timer = QTimer()
        self.savedata_timer.timeout.connect(self.data.save_data)
        self.savedata_timer.start(1000*60*1)

        # data aggregate timer
        self.aggdata_timer = QTimer()
        self.aggdata_timer.timeout.connect(self.data.aggregate_data)
        self.aggdata_timer.start(10000)

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

        # # ui update timers
        # self.dashboard_timer = QTimer()
        # self.dashboard_timer.timeout.connect(self.update_dashboard)
        # self.dashboard_timer.start(1000 * 5)
        #
        # self.daily_timer = QTimer()
        # self.daily_timer.timeout.connect(self.update_daily)
        # self.daily_timer.start(1000 * 5)
        #
        # self.weekly_timer = QTimer()
        # self.weekly_timer.timeout.connect(self.update_weekly)
        # self.weekly_timer.start(1000 * 60 * 5)
        #
        # self.yearly_timer = QTimer()
        # self.yearly_timer.timeout.connect(self.update_yearly)
        # self.yearly_timer.start(1000 * 60 * 60 * 1)
        #
        # self.all_timer = QTimer()
        # self.all_timer.timeout.connect(self.update_all)
        # self.all_timer.start(1000 * 60 * 60 * 1)
        #
        # # create curves for all the plots
        # self.plotcurves = {"daily": {}, "weekly": {}, "yearly": {}, "all": {}}
        #
        # self.plotcurves["daily"]['temp'] = self.tempDailyGraph.plot(np.array([0]))
        # self.plotcurves["daily"]['hum'] = self.humDailyGraph.plot(np.array([0]))
        # self.plotcurves["daily"]['wind'] = self.windDailyGraph.plot(np.array([0]))
        # self.plotcurves["daily"]['rain'] = self.rainDailyGraph.plot(np.array([0]))

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
