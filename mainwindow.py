# This Python file uses the following encoding: utf-8

import sys

from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QObject
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic

from datasources import SinData, CosData, Generator
from dataprocessor import DataProcessor


class MainWindow(QMainWindow):
    """   """
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = uic.loadUi('MainWindow.ui', self)

        self.window_str = "None"
        self.frq_founded = 0.0

        self.buttonExit.clicked.connect(self.on_exit_button)
        self.buttonExit.clicked.connect(QApplication.instance().quit)

        self.data_source = Generator(100, self)
        self.data_source.data_ready.connect(self.on_data1_ready)
        self.srcControlWidget.set_model(self.data_source)




        self.data_proc = DataProcessor(1024, 'None', 'None')
        self.data_source.data_ready.connect(self.data_proc.on_data_recv)
        self.data_proc.data_processed.connect(self.on_data2_ready)


        self.controlWidget.window_changed_str.connect(self.data_proc.on_wind_changed)
        self.controlWidget.method_changed_str.connect(self.data_proc.on_method_changed)

        self.data_proc.data_processed.connect(self.on_freq_status)
        #self.data_proc.data_processed.connect(self.on_freq_founded)

        self.srcControlWidget.params_changed.connect(self.data_source.on_params_changed)


        #self.data_source = CosData(8192, 10, self)
        #self.data_source.data_ready.connect(self.on_data2_ready)

        self.data_curve1 = self.ui.plot1.plot(title = 'Generated signal plot')
        self.data_curve2 = self.ui.plot2.plot(title = 'Fourier Transform plot')
        self.data_curve3 = self.ui.plot3.plot(title = 'Test plot')

        self.ui.freq_show.setStyleSheet("QLCDNumber {color: red;}")
        self.ui.freq_show.setFixedWidth(300)

    def on_exit_button(self):
        print(self, ' Exiting... Bye...')

    def on_data1_ready(self, data_source):
        self.data_curve1.setData(data_source.dataX, data_source.dataY)

    def on_data2_ready(self, data_processor):
        """   """
        """ draw Fourier spectra """
        self.data_curve2.setData(data_processor.fftwX, data_processor.fftwY)
        # self.data_curve2.setData(data_source.dataX, data_source.dataY)

        """ draw naff function for tests """
        if data_processor.alpha is not None:
            if data_processor.falpha is not None:
                self.data_curve3.setData(data_processor.alpha, data_processor.falpha)

    def on_freq_status(self, data_processor):
        if data_processor.warning == 0:
            self.ui.freq_stat.setText('Frequency = {}'.format(data_processor.frq_founded))
        elif data_processor.warning == 1:
            self.ui.freq_stat.setText(data_processor.warningText)
        else:
            self.ui.freq_stat.setText('Warning number has unexpected value!')

        freq_text = '{}'.format(data_processor.frq_founded)
        self.ui.freq_show.display(freq_text)

    def init_plots(self):
        """   """
        self.ui.data_plot.showGrid(x = True, y = True)
        self.ui.fftw_plot.showGrid(x = True, y = True)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
