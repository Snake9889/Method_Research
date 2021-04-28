#
#
#

from PyQt5.QtCore import pyqtSignal, Qt, QObject, QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QGridLayout

import numpy as np


class SinData(QObject):
    """   """
    data_ready = pyqtSignal(object)

    def __init__(self, data_len = 1024, def_time = 1000, parent = None):
        super(SinData, self).__init__(parent)

        self.timer = QTimer()
        self.timer.timeout.connect(self.on_timer_update)
        self.timer.start(def_time)

        self.data_len = data_len
        self.dataX = None
        self.dataY = None

    def on_timer_update(self):
        self.dataX = np.arange(0, self.data_len, dtype=float)
        self.dataY = np.sin(2 * np.pi * 0.17 * self.dataX) + 0.05 * np.random.normal(size=self.data_len)

        self.data_ready.emit(self)

    def on_params_changed(self, params_dict):
        print(params_dict)


class CosData(QObject):
    """   """
    data_ready = pyqtSignal(object)

    def __init__(self, data_len = 1024, def_time = 1000, parent = None):
        super(CosData, self).__init__(parent)

        self.timer = QTimer()
        self.timer.timeout.connect(self.on_timer_update)
        self.timer.start(1000)

        self.data_len = data_len
        self.dataX = None
        self.dataY = None

    def on_timer_update(self):
        self.dataX = np.arange(0, self.data_len, dtype=float)
        self.dataY = np.cos(2 * np.pi * 0.17 * self.dataX) + 0.05 * np.random.normal(size=self.data_len)

        self.data_ready.emit(self)

    def on_params_changed(self, params_dict):
        print(params_dict)


class Generator(QObject):
    """   """
    data_ready = pyqtSignal(object)

    def __init__(self, def_time = 1000, parent = None):
        super(Generator, self).__init__(parent)

        self.timer = QTimer()
        self.timer.timeout.connect(self.on_timer_update)
        self.timer.start(def_time)

        # main parameters
        self.signal_types = ('None', 'Sin', 'Cos', 'ExpSin', 'ExpCos')

        self.params = {
            'type': 'Sin',
            'num': 1024,
            'amp': 2.0,
            'frq': 0.2,
            'phs': 0.1,
            'dec': 27.0,
            'noise': 0.05,
            'lboard': 0.0,
            'rboard': 0.5
        }

        self.dataX = None
        self.dataY = None

        self.data_len = 1024
        self.rboard = 0.5
        self.lboard = 0.0

        self.data_gen()

    def on_timer_update(self):
        """   """
        self.data_gen()
        self.data_ready.emit(self)

    def data_gen(self):
        """   """
        stype = self.params.get('type', 'Cos')
        num = self.params.get('num', 1024)
        amp = self.params.get('amp', 2.0)
        frq = self.params.get('frq', 0.2)
        phs = self.params.get('phs', 0.1)
        dec = self.params.get('dec', 1.0)
        noise = self.params.get('noise', 0.01)
        lboard = self.params.get('lboard', 0.0)
        rboard = self.params.get('rboard', 0.5)

        self.data_len = num
        self.rboard = rboard
        self.lboard = lboard

        self.dataX = np.arange(0, self.data_len, dtype=float)

        if stype == 'None':
            self.dataY = np.ones(self.data_len)
        elif stype == 'Sin':
            self.dataY = np.sin(2 * np.pi * frq * self.dataX + phs) + np.sin(2 * np.pi * 1.2 * frq * self.dataX + phs)
        elif stype == 'Cos':
            self.dataY = np.cos(2 * np.pi * frq * self.dataX + phs)
        elif stype == 'ExpSin':
            self.dataY = np.exp(-1 * dec * 10.0e-8 * self.dataX * self.dataX) * np.sin(2 * np.pi * frq * self.dataX + phs)
        elif stype == 'ExpCos':
            self.dataY = np.exp(-1 * dec * 10.0e-8 * self.dataX * self.dataX) * np.cos(2 * np.pi * frq * self.dataX + phs)
        else:
            self.dataY = np.zeros(self.data_len)

        self.dataY = amp * self.dataY

        self.dataY = self.dataY + noise * amp * np.random.normal(size=self.data_len)

    def on_params_changed(self, params_dict):
        print(params_dict)
        self.params = params_dict
