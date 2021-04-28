# This Python file uses the following encoding: utf-8
#
import signal
import sys

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QGridLayout
from PyQt5 import uic

import numpy as np
import pyqtgraph as pg

from mainwindow import *

#from numpy.fft import rfft, rfftfreq

pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')


# Allow CTRL+C and/or SIGTERM to kill us (PyQt blocks it otherwise)
signal.signal(signal.SIGINT, signal.SIG_DFL)
signal.signal(signal.SIGTERM, signal.SIG_DFL)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)

    mw = MainWindow()

    mw.show()
    sys.exit(app.exec_())
