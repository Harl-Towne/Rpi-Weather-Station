import sys

import numpy as np
import pandas as pd
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMainWindow, QGridLayout

import main_ui

import pyqtgraph as pg
import matplotlib

from threadqueue import threadqueuing

matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from datamanagment.datagrabber import get_data
from datamanagment.weatherdatamanager import WeatherData
from time import sleep
from pprint import pprint


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
            self.data = WeatherData(agg_intervals=(pd.Timedelta("60S"), pd.Timedelta("300S"), pd.Timedelta("1800S")))
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
        self.aggdata_timer.start(1000*60*5)
        self.data.aggregate_data()

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

        # ui update timers
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

        # create plots and add into window
        self.axes = {"daily": {}, "weekly": {}, "yearly": {}, "all": {}}  # for updating data
        self.figures = {"daily": {}, "weekly": {}, "yearly": {}, "all": {}}  # for triggering redraw
        layouts = [self.Daily_Graphs.layout(), self.Weekly_Graphs.layout(), self.Yearly_Graphs.layout(), self.All_Time_Graphs.layout()]
        for i, layout in enumerate(layouts):
            key = list(self.axes.keys())[i]

            self.figures[key]['temp'] = Figure()
            self.figures[key]['hum'] = Figure()
            self.figures[key]['wind'] = Figure()
            self.figures[key]['rain'] = Figure()

            c1 = FigureCanvas(self.figures[key]['temp'])
            c2 = FigureCanvas(self.figures[key]['hum'])
            c3 = FigureCanvas(self.figures[key]['wind'])
            c4 = FigureCanvas(self.figures[key]['rain'])

            self.axes[key]['temp'] = self.figures[key]['temp'].add_subplot(111)
            self.axes[key]['hum'] = self.figures[key]['hum'].add_subplot(111)
            self.axes[key]['wind'] = self.figures[key]['wind'].add_subplot(111)
            self.axes[key]['rain'] = self.figures[key]['rain'].add_subplot(111)

            self.axes[key]['temp'].autoscale(enable=True, axis='both', tight=True)
            self.axes[key]['hum'].autoscale(enable=True, axis='both', tight=True)
            self.axes[key]['wind'].autoscale(enable=True, axis='both', tight=True)
            self.axes[key]['rain'].autoscale(enable=True, axis='both', tight=True)

            layout.addWidget(c1, 0, 0, 1, 1)
            layout.addWidget(c2, 0, 1, 1, 1)
            layout.addWidget(c3, 1, 0, 1, 1)
            layout.addWidget(c4, 1, 1, 1, 1)

    def toolbar_clicked(self, btn_no):
        self.stackedWidget.setCurrentIndex(btn_no)
        if btn_no == 1:
            self.update_daily()
        elif btn_no == 2:
            self.update_weekly()
        elif btn_no == 3:
            self.update_yearly()
        elif btn_no == 4:
            self.update_all()

    def update_dashboard(self):
        latest_data = self.data.rt_data.iloc[-1, :]
        self.currentTempFeild.setText(str(latest_data["temperature"]))
        self.currenthumFeild.setText(str(latest_data["humidity"]))
        self.windSpeedFeild.setText(str(latest_data["wind_speed"]))
        self.windDirectFeild.setText(self.wind_directions[int(latest_data["wind_direction"])])
        self.dayRainFeild.setText(str(latest_data["rain"]))

    @threadqueuing
    def update_daily(self):
        print(self.axes)
        print(self.data)
        print(self.figures)
        self.axes["daily"]["temp"].clear()
        self.axes["daily"]["hum"].clear()
        self.axes["daily"]["wind"].clear()
        self.axes["daily"]["rain"].clear()

        x = self.data.rt_data.loc[:, "datetime"].to_numpy()

        self.axes["daily"]["temp"].plot(x, np.array(self.data.rt_data.loc[:, "temperature"].to_numpy(), dtype=float))
        self.axes["daily"]["hum"].plot(x, np.array(self.data.rt_data.loc[:, "humidity"].to_numpy(), dtype=float))
        self.axes["daily"]["wind"].plot(x, np.array(self.data.rt_data.loc[:, "wind_speed"].to_numpy(), dtype=float))
        self.axes["daily"]["rain"].plot(x, np.array(self.data.rt_data.loc[:, "rain"].to_numpy(), dtype=float))

        self.axes["daily"]['temp'].autoscale(enable=True, axis='both', tight=True)
        self.axes["daily"]['hum'].autoscale(enable=True, axis='both', tight=True)
        self.axes["daily"]['wind'].autoscale(enable=True, axis='both', tight=True)
        self.axes["daily"]['rain'].autoscale(enable=True, axis='both', tight=True)

        self.figures["daily"]["temp"].canvas.draw()
        self.figures["daily"]["hum"].canvas.draw()
        self.figures["daily"]["wind"].canvas.draw()
        self.figures["daily"]["rain"].canvas.draw()

    @threadqueuing
    def update_weekly(self):
        self.axes["weekly"]["temp"].clear()
        self.axes["weekly"]["hum"].clear()
        self.axes["weekly"]["wind"].clear()
        self.axes["weekly"]["rain"].clear()

        data = self.data.agg_data[0]
        x = data.loc[:, "datetime"].to_numpy()

        self.axes["weekly"]["temp"].plot(x, np.array(data.loc[:, "avg_temperature"].to_numpy(), dtype=float))
        self.axes["weekly"]["hum"].plot(x, np.array(data.loc[:, "avg_humidity"].to_numpy(), dtype=float))
        self.axes["weekly"]["wind"].plot(x, np.array(data.loc[:, "avg_wind_speed"].to_numpy(), dtype=float))
        self.axes["weekly"]["rain"].plot(x, np.array(data.loc[:, "rain"].to_numpy(), dtype=float))

        self.axes["weekly"]['temp'].autoscale(enable=True, axis='both', tight=True)
        self.axes["weekly"]['hum'].autoscale(enable=True, axis='both', tight=True)
        self.axes["weekly"]['wind'].autoscale(enable=True, axis='both', tight=True)
        self.axes["weekly"]['rain'].autoscale(enable=True, axis='both', tight=True)

        self.figures["weekly"]["temp"].canvas.draw()
        self.figures["weekly"]["hum"].canvas.draw()
        self.figures["weekly"]["wind"].canvas.draw()
        self.figures["weekly"]["rain"].canvas.draw()

    @threadqueuing
    def update_yearly(self):
        self.axes["yearly"]["temp"].clear()
        self.axes["yearly"]["hum"].clear()
        self.axes["yearly"]["wind"].clear()
        self.axes["yearly"]["rain"].clear()

        data = self.data.agg_data[1]
        x = data.loc[:, "datetime"].to_numpy()

        self.axes["yearly"]["temp"].plot(x, np.array(data.loc[:, "avg_temperature"].to_numpy(), dtype=float))
        self.axes["yearly"]["hum"].plot(x, np.array(data.loc[:, "avg_humidity"].to_numpy(), dtype=float))
        self.axes["yearly"]["wind"].plot(x, np.array(data.loc[:, "avg_wind_speed"].to_numpy(), dtype=float))
        self.axes["yearly"]["rain"].plot(x, np.array(data.loc[:, "rain"].to_numpy(), dtype=float))

        self.axes["yearly"]['temp'].autoscale(enable=True, axis='both', tight=True)
        self.axes["yearly"]['hum'].autoscale(enable=True, axis='both', tight=True)
        self.axes["yearly"]['wind'].autoscale(enable=True, axis='both', tight=True)
        self.axes["yearly"]['rain'].autoscale(enable=True, axis='both', tight=True)

        self.figures["yearly"]["temp"].canvas.draw()
        self.figures["yearly"]["hum"].canvas.draw()
        self.figures["yearly"]["wind"].canvas.draw()
        self.figures["yearly"]["rain"].canvas.draw()

    @threadqueuing
    def update_all(self):
        self.axes["all"]["temp"].clear()
        self.axes["all"]["hum"].clear()
        self.axes["all"]["wind"].clear()
        self.axes["all"]["rain"].clear()

        data = self.data.agg_data[2]
        x = data.loc[:, "datetime"].to_numpy()

        self.axes["all"]["temp"].plot(x, np.array(data.loc[:, "avg_temperature"].to_numpy(), dtype=float))
        self.axes["all"]["hum"].plot(x, np.array(data.loc[:, "avg_humidity"].to_numpy(), dtype=float))
        self.axes["all"]["wind"].plot(x, np.array(data.loc[:, "avg_wind_speed"].to_numpy(), dtype=float))
        self.axes["all"]["rain"].plot(x, np.array(data.loc[:, "rain"].to_numpy(), dtype=float))

        self.axes["all"]['temp'].autoscale(enable=True, axis='both', tight=True)
        self.axes["all"]['hum'].autoscale(enable=True, axis='both', tight=True)
        self.axes["all"]['wind'].autoscale(enable=True, axis='both', tight=True)
        self.axes["all"]['rain'].autoscale(enable=True, axis='both', tight=True)

        self.figures["all"]["temp"].canvas.draw()
        self.figures["all"]["hum"].canvas.draw()
        self.figures["all"]["wind"].canvas.draw()
        self.figures["all"]["rain"].canvas.draw()
