import sys
from random import randint
from time import sleep

from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import QTimer, pyqtSlot, QRunnable, QThreadPool, pyqtSignal

from qt_ui import main_ui
from randomclass import randomClass
from threadqueue import workerGeneric, threadQueue


class mainWindow(QMainWindow, main_ui.Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self, **kwargs):
        super(mainWindow, self).setupUi(self)

        # connect all toolbar buttons to actions
        self.actionDashboard.triggered.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.actionDaily_Graphs.triggered.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.actionWeekly_Graphs.triggered.connect(lambda: self.stackedWidget.setCurrentIndex(2))
        self.actionYearly_Graphs.triggered.connect(lambda: self.stackedWidget.setCurrentIndex(3))
        self.actionAll_Time_Graphs.triggered.connect(lambda: self.stackedWidget.setCurrentIndex(4))
        self.actionSettings.triggered.connect(lambda: self.stackedWidget.setCurrentIndex(5))
        self.actionExit.triggered.connect(lambda: sys.exit())

        self.t1 = QTimer()
        self.t1.setInterval(1000)
        self.t1.timeout.connect(lambda: print("t1"))

        self.t2 = QTimer()
        self.t2.setInterval(500)
        self.t2.timeout.connect(lambda: print("t2"))

        self.pushButton.clicked.connect(lambda: self.t1.start())
        self.pushButton_2.clicked.connect(lambda: self.t2.start())

        self.pushButton_3.clicked.connect(self.run_blocker)
        self.n = 0

    def run_blocker(self):
        r = randomClass(a=2, b=2)
        r.block()
