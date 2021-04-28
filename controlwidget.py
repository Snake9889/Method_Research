# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 17:53:07 2019

@author: Вячеслав
"""

from PyQt5.QtCore import pyqtSignal, Qt, QObject
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QGridLayout

from PyQt5 import uic


class ControlWidget(QWidget):
    """   """
    window_changed_str = pyqtSignal(str)
    window_changed_obj = pyqtSignal(object)
    method_changed_str = pyqtSignal(str)
    method_changed_obj = pyqtSignal(object)

    def __init__(self, parent = None):
        super(ControlWidget, self).__init__(parent)
        self.ui = uic.loadUi('ControlWidget.ui', self)

        self.window = "None"
        self.method = "None"

        buttons = [
            self.usePeakBtn,
            self.useGassiorBtn,
            self.useNaffBtn,
        ]

        id = 1
        for btn in buttons:
            btn.setStyleSheet("QPushButton {background-color: none}"
                              "QPushButton:checked {background-color: green}")
            self.buttonGroup.setId(btn, id)
            id = id + 1

        self.checkWindowBox.currentIndexChanged.connect(self.on_window_checked)
        self.buttonGroup.buttonClicked['int'].connect(self.on_method_checked)

    def on_window_checked(self, state):
        """   """
        #print('window_box_state = ', state)

        if state == 0:
            self.window = "None"
        elif state == 1:
            self.window = "Hann"
        elif state == 2:
            self.window = "Hamming"
        else:
            self.window = "None"

        self.window_changed_str.emit(self.window)
        self.window_changed_obj.emit(self)

    def on_method_checked(self, state):
        """   """
        print('method_state = ', state)

        if state == 0:
            self.method = "None"
        elif state == 1:
            self.method = "Peak"
        elif state == 2:
            self.method = "Gassior"
        elif state == 3:
            self.method = "Naff"
        else:
            self.method = "None"

        self.method_changed_str.emit(self.method)
        self.method_changed_obj.emit(self)




