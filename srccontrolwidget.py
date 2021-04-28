# -*- coding: utf-8 -*-
"""
Created on Fri Nov 30 04:22:50 2019

@author: Вячеслав
"""

from PyQt5.QtCore import pyqtSignal, Qt, QObject
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QGridLayout

from PyQt5 import uic

from datasources import Generator


class SrcControlWidget(QWidget):
    """   """
    params_changed = pyqtSignal(object)

    def __init__(self, parent = None):
        super(SrcControlWidget, self).__init__(parent)
        self.ui = uic.loadUi('SrcControlWidget.ui', self)

        self.type = "Sin"
        self.num = 1024
        self.amp = 1.0
        self.frq = 0.2
        self.phs = 0.1
        self.dec = 1.0
        self.noise = 0.1
        self.lboard = 0.15
        self.rboard = 0.2

        self.params = None
        self.source_model = None

        self.sigTBox.currentIndexChanged.connect(self.on_sigtbox_changed)
        self.numSBox.valueChanged.connect(self.on_numsbox_changed)
        self.ampSBox.valueChanged.connect(self.on_ampsbox_changed)
        self.frqSBox.valueChanged.connect(self.on_frqsbox_changed)
        self.phsSBox.valueChanged.connect(self.on_phssbox_changed)
        self.decSBox.valueChanged.connect(self.on_decsbox_changed)
        self.noiseSBox.valueChanged.connect(self.on_noisesbox_changed)
        self.lboardSBox.valueChanged.connect(self.on_lboardsbox_changed)
        self.rboardSBox.valueChanged.connect(self.on_rboardsbox_changed)

    def set_model(self, data_source_model):
        """   """
        self.source_model = data_source_model

        for value in self.source_model.signal_types:
            self.sigTBox.addItem(value)

        self.sigTBox.setCurrentIndex(1)
        self.numSBox.setValue(self.source_model.params['num'])
        self.ampSBox.setValue(self.source_model.params['amp'])
        self.frqSBox.setValue(self.source_model.params['frq'])
        self.phsSBox.setValue(self.source_model.params['phs'])
        self.decSBox.setValue(self.source_model.params['dec'])
        self.noiseSBox.setValue(self.source_model.params['noise'])
        self.lboardSBox.setValue(self.source_model.params['lboard'])
        self.rboardSBox.setValue(self.source_model.params['rboard'])

        self.params = self.source_model.params

        self.deliver_params()

    def on_numsbox_changed(self, value):
        self.num = value
        # self.params['num'] = value
        self.deliver_params()

    def on_ampsbox_changed(self, value):
        self.amp = value
        self.deliver_params()

    def on_frqsbox_changed(self, value):
        self.frq = value
        self.deliver_params()

    def on_phssbox_changed(self, value):
        self.phs = value
        self.deliver_params()

    def on_decsbox_changed(self, value):
        self.dec = value
        self.deliver_params()

    def on_noisesbox_changed(self, value):
        self.noise = value
        self.deliver_params()

    def deliver_params(self):
        """   """
        self.params = {
            "type": self.type,
            "num" : self.num,
            "amp" : self.amp,
            "frq" : self.frq,
            "phs" : self.phs,
            "dec" : self.dec,
            "noise" : self.noise,
            "lboard": self.lboard,
            "rboard": self.rboard
        }
        self.params_changed.emit(self.params)

    def on_sigtbox_changed(self, state):
        """   """
        if state == 0:
            self.type = "None"
        elif state == 1:
            self.type = "Sin"
        elif state == 2:
            self.type = "Cos"
        elif state == 3:
            self.type = "ExpSin"
        elif state == 4:
            self.type = "ExpCos"
        else:
            self.type = "Sin"

        self.deliver_params()

    def on_lboardsbox_changed(self, value):
        """   """
        self.lboard = value
        print(self.lboard)
        self.deliver_params()

    def on_rboardsbox_changed(self, value):
        """   """
        self.rboard = value
        self.deliver_params()

