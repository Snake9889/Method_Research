# -*- coding: utf-8 -*-
"""
Created on Sun Nov 23 04:35:20 2019

@author: Вячеслав
"""

from PyQt5.QtCore import pyqtSignal, Qt, QObject, QTimer
import numpy as np
import math


class DataProcessor(QObject):
    """   """
    data_processed = pyqtSignal(object)

    def __init__(self, data_len = 1024, window = 'None', alg = 'Gassior', lboard = 0.0, rboard = 0.5, parent = None):
        super(DataProcessor, self).__init__(parent)

        self.windowType = window
        self.data_len = data_len
        self.algType = alg
        self.window = None

        self.regen_wind(self.windowType)

        self.left_bound = lboard
        self.right_bound = rboard

        self.dataX = None
        self.dataY = None

        self.fftwX = None
        self.fftwY = None

        self.alpha = None
        self.falpha = None

        self.frq_founded = 0.0

        self.warning = 0
        self.warningText = ""

    def on_wind_changed(self, windowType):
        """   """
        self.windowType = windowType
        self.regen_wind(self.windowType)

    def on_method_changed(self, algType):
        """   """
        self.algType = algType

    def regen_wind(self, windowType):
        """   """
        if windowType == 'None':
            self.window = np.ones(self.data_len)
        if windowType == 'Hann':
            self.window = np.hanning(self.data_len)
        if windowType == 'Hamming':
            self.window = np.hamming(self.data_len)

    def on_data_recv(self, data_source):
        """   """
        self.data_len = data_source.data_len
        self.regen_wind(self.windowType)

        self.dataX = data_source.dataX
        self.dataY = data_source.dataY

        self.dataY = self.dataY * self.window

        self.left_bound = data_source.lboard
        self.right_bound = data_source.rboard
        print(self.left_bound, self.right_bound)

        self.fftwX = np.fft.rfftfreq(self.data_len, 1.)
        self.fftwY = np.abs(np.fft.rfft(self.dataY)) / self.data_len

        if self.algType == 'None':
            self.frq_founded = 0.0
            self.warning = 0
            self.warningText = 'No warnings!'

        if self.algType == 'Peak':
            self.frq_founded = self.on_peak_method()
            print('[', self.algType, '] Freq founded = ', self.frq_founded)

        if self.algType == 'Gassior':
            self.frq_founded = self.on_gassior_method()
            print('[', self.algType, '] Freq founded = ', self.frq_founded)

        if self.algType == 'Naff':
            self.frq_founded = self.on_naff_method()
            print('[', self.algType, '] Freq founded = ', self.frq_founded)

        self.data_processed.emit(self)

    def on_peak_method(self):
        """   """
        left_ind = math.floor(self.data_len * self.left_bound)
        right_ind = math.ceil(self.data_len * self.right_bound)

        tmp_x = self.fftwX[left_ind: right_ind]
        tmp_y = self.fftwY[left_ind: right_ind]

        ind = np.argmax(tmp_y)

        self.frq_founded = tmp_x[ind]
        self.warning = 0
        self.warningText = 'No warnings!'

        return self.frq_founded

    def on_gassior_method(self):
        """   """
        left_ind = math.floor(self.data_len * self.left_bound)
        right_ind = math.ceil(self.data_len * self.right_bound)

        tmp_x = self.fftwX[left_ind : right_ind]
        tmp_y = self.fftwY[left_ind : right_ind]

        ind0 = np.argmax(tmp_y)
        indl = ind0 - 1
        indr = ind0 + 1

        if ind0 == 0 or ind0 == len(tmp_x) - 1:
            self.frq_founded = self.on_peak_method()
            self.warning = 1
            self.warningText = '[Gassior] index of the founded frequency peak is on the left or right border!'
            print(self.warningText)
        else:
            self.frq_founded = tmp_x[ind0] + (tmp_y[indr] - tmp_y[indl]) /\
                            (2 * self.data_len * (2 * tmp_y[ind0] - tmp_y[indl] - tmp_y[indr]))
            self.warning = 0
            self.warningText = 'No warnings!'

        return self.frq_founded

    def on_naff_method(self):
        """   """
        left_ind = math.floor(self.data_len * self.left_bound)
        right_ind = math.ceil(self.data_len * self.right_bound)

        tmp_y = self.fftwY[left_ind: right_ind]
        tmp_x = self.fftwX[left_ind: right_ind]

        ind0 = np.argmax(tmp_y)

        if ind0 == 0:
            indl = ind0
            indr = ind0 + 1

            self.warning = 1
            self.warningText = '[Naff] index of the founded frequency peak is on the left border!'
            print(self.warningText)
        elif ind0 == len(tmp_x) - 1:
            indl = ind0 - 1
            indr = ind0

            self.warning = 1
            self.warningText = '[Naff] index of the founded frequency peak is on the right border!'
            print(self.warningText)
        else:
            indl = ind0 - 1
            indr = ind0 + 1

            self.warning = 0
            self.warningText = 'No warnings!'

        self.frq_founded = tmp_x[ind0]
        frql = tmp_x[indl]
        frqr = tmp_x[indr]
        print('Naff now', 'ind0 = ', ind0, 'len_tmp_x = ', len(tmp_x), frql, self.frq_founded, frqr)

        alpha = np.arange(frql, frqr, 1.0e-5)
        falpha = np.copy(alpha)

        for it in range(len(alpha)):
            """   """
            omega = alpha[it]

            if False:
                conv_exp = np.exp(2 * np.pi * complex(0, 1) * self.dataX * omega)
                falpha[it] = np.sum(np.abs(conv_exp * self.dataY))
            else:
                conv_cos = np.sum( np.cos(2 * np.pi * self.dataX * omega) * self.dataY )
                conv_sin = np.sum( np.sin(2 * np.pi * self.dataX * omega) * self.dataY )
                falpha[it] = np.sqrt( conv_cos * conv_cos + conv_sin * conv_sin )

        self.alpha = alpha.copy()
        self.falpha = falpha.copy()

        ind_alpha = np.argmax(self.falpha)
        self.frq_founded = self.alpha[ind_alpha]

        return self.frq_founded
