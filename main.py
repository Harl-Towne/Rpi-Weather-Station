import sys
import traceback

from PyQt5.QtWidgets import QApplication
import mainweatherapp

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    win = mainweatherapp.mainWeatherWindow()
    # win.showFullScreen()
    # win.show()
    sys.exit(app.exec())
