#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: N210 source
# Author: David Badger
# Description: UHF filtering
# GNU Radio version: 3.8.2.0

from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from PyQt5 import Qt
from PyQt5.QtCore import QObject, pyqtSlot
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import gr
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import uhd
import time
from gnuradio.qtgui import Range, RangeWidget

from gnuradio import qtgui

class UHD_N210_fosphor_rev2(gr.top_block, Qt.QWidget):

    def __init__(self, gain=0):
        gr.top_block.__init__(self, "N210 source")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("N210 source")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "UHD_N210_fosphor_rev2")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Parameters
        ##################################################
        self.gain = gain

        ##################################################
        # Variables
        ##################################################
        self.update = update = .01
        self.samp_rate2 = samp_rate2 = 30000000
        self.samp_rate = samp_rate = 1e6
        self.samp_1 = samp_1 = 1e6
        self.low_0 = low_0 = -125
        self.hi_0 = hi_0 = 5
        self.gain_0 = gain_0 = 3
        self.freq_1 = freq_1 = 433.65e6
        self.freq = freq = 443.025e6
        self.fft_0 = fft_0 = 1024
        self.cf = cf = 15000000
        self.antenna = antenna = "RX2"

        ##################################################
        # Blocks
        ##################################################
        self._update_range = Range(.00001, .05, .00005, .01, 200)
        self._update_win = RangeWidget(self._update_range, self.set_update, 'update', "counter_slider", float)
        self.top_grid_layout.addWidget(self._update_win)
        self._samp_1_range = Range(1e6, 50e6, 1e6, 1e6, 200)
        self._samp_1_win = RangeWidget(self._samp_1_range, self.set_samp_1, 'sample_rate', "counter_slider", float)
        self.top_grid_layout.addWidget(self._samp_1_win)
        self._low_0_range = Range(-200, -60, 1, -125, 200)
        self._low_0_win = RangeWidget(self._low_0_range, self.set_low_0, 'low', "counter_slider", float)
        self.top_grid_layout.addWidget(self._low_0_win)
        self._hi_0_range = Range(-100, 100, 1, 5, 200)
        self._hi_0_win = RangeWidget(self._hi_0_range, self.set_hi_0, 'hi', "counter_slider", float)
        self.top_grid_layout.addWidget(self._hi_0_win)
        self._gain_0_range = Range(0, 60, 1, 3, 200)
        self._gain_0_win = RangeWidget(self._gain_0_range, self.set_gain_0, 'Gain', "counter_slider", float)
        self.top_grid_layout.addWidget(self._gain_0_win)
        self._freq_1_range = Range(100e6, 3000e6, 100e3, 433.65e6, 200)
        self._freq_1_win = RangeWidget(self._freq_1_range, self.set_freq_1, 'Freq', "counter_slider", float)
        self.top_grid_layout.addWidget(self._freq_1_win)
        self._fft_0_range = Range(1024, 7168, 1024, 1024, 200)
        self._fft_0_win = RangeWidget(self._fft_0_range, self.set_fft_0, 'FFT', "counter_slider", int)
        self.top_grid_layout.addWidget(self._fft_0_win)
        self.uhd_usrp_source_0_0 = uhd.usrp_source(
            ",".join(("", "")),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,1)),
            ),
        )
        self.uhd_usrp_source_0_0.set_center_freq(freq_1, 0)
        self.uhd_usrp_source_0_0.set_gain(gain_0, 0)
        self.uhd_usrp_source_0_0.set_antenna('RX2', 0)
        self.uhd_usrp_source_0_0.set_samp_rate(samp_1)
        self.uhd_usrp_source_0_0.set_time_unknown_pps(uhd.time_spec())
        self.qtgui_waterfall_sink_x_0 = qtgui.waterfall_sink_c(
            fft_0, #size
            firdes.WIN_BLACKMAN_hARRIS, #wintype
            freq_1, #fc
            samp_1, #bw
            "", #name
            1 #number of inputs
        )
        self.qtgui_waterfall_sink_x_0.set_update_time(update)
        self.qtgui_waterfall_sink_x_0.enable_grid(False)
        self.qtgui_waterfall_sink_x_0.enable_axis_labels(True)



        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_0.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_0.set_line_alpha(i, alphas[i])

        self.qtgui_waterfall_sink_x_0.set_intensity_range(low_0, hi_0)

        self._qtgui_waterfall_sink_x_0_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_waterfall_sink_x_0_win)
        # Create the options list
        self._antenna_options = ("TX/RX", "RX2", )
        # Create the labels list
        self._antenna_labels = ("TX/RX", "RX2", )
        # Create the combo box
        self._antenna_tool_bar = Qt.QToolBar(self)
        self._antenna_tool_bar.addWidget(Qt.QLabel('Antenna' + ": "))
        self._antenna_combo_box = Qt.QComboBox()
        self._antenna_tool_bar.addWidget(self._antenna_combo_box)
        for _label in self._antenna_labels: self._antenna_combo_box.addItem(_label)
        self._antenna_callback = lambda i: Qt.QMetaObject.invokeMethod(self._antenna_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._antenna_options.index(i)))
        self._antenna_callback(self.antenna)
        self._antenna_combo_box.currentIndexChanged.connect(
            lambda i: self.set_antenna(self._antenna_options[i]))
        # Create the radio buttons
        self.top_grid_layout.addWidget(self._antenna_tool_bar)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.uhd_usrp_source_0_0, 0), (self.qtgui_waterfall_sink_x_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "UHD_N210_fosphor_rev2")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain

    def get_update(self):
        return self.update

    def set_update(self, update):
        self.update = update
        self.qtgui_waterfall_sink_x_0.set_update_time(self.update)

    def get_samp_rate2(self):
        return self.samp_rate2

    def set_samp_rate2(self, samp_rate2):
        self.samp_rate2 = samp_rate2

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate

    def get_samp_1(self):
        return self.samp_1

    def set_samp_1(self, samp_1):
        self.samp_1 = samp_1
        self.qtgui_waterfall_sink_x_0.set_frequency_range(self.freq_1, self.samp_1)
        self.uhd_usrp_source_0_0.set_samp_rate(self.samp_1)

    def get_low_0(self):
        return self.low_0

    def set_low_0(self, low_0):
        self.low_0 = low_0
        self.qtgui_waterfall_sink_x_0.set_intensity_range(self.low_0, self.hi_0)

    def get_hi_0(self):
        return self.hi_0

    def set_hi_0(self, hi_0):
        self.hi_0 = hi_0
        self.qtgui_waterfall_sink_x_0.set_intensity_range(self.low_0, self.hi_0)

    def get_gain_0(self):
        return self.gain_0

    def set_gain_0(self, gain_0):
        self.gain_0 = gain_0
        self.uhd_usrp_source_0_0.set_gain(self.gain_0, 0)

    def get_freq_1(self):
        return self.freq_1

    def set_freq_1(self, freq_1):
        self.freq_1 = freq_1
        self.qtgui_waterfall_sink_x_0.set_frequency_range(self.freq_1, self.samp_1)
        self.uhd_usrp_source_0_0.set_center_freq(self.freq_1, 0)

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq

    def get_fft_0(self):
        return self.fft_0

    def set_fft_0(self, fft_0):
        self.fft_0 = fft_0

    def get_cf(self):
        return self.cf

    def set_cf(self, cf):
        self.cf = cf

    def get_antenna(self):
        return self.antenna

    def set_antenna(self, antenna):
        self.antenna = antenna
        self._antenna_callback(self.antenna)




def argument_parser():
    description = 'UHF filtering'
    parser = ArgumentParser(description=description)
    parser.add_argument(
        "--gain", dest="gain", type=eng_float, default="0.0",
        help="Set gain [default=%(default)r]")
    return parser


def main(top_block_cls=UHD_N210_fosphor_rev2, options=None):
    if options is None:
        options = argument_parser().parse_args()

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls(gain=options.gain)

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    def quitting():
        tb.stop()
        tb.wait()

    qapp.aboutToQuit.connect(quitting)
    qapp.exec_()

if __name__ == '__main__':
    main()
