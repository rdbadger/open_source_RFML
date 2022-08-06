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
import sip
from gnuradio import fosphor
from gnuradio.fft import window
from gnuradio import gr
from gnuradio.filter import firdes
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import uhd
import time

from gnuradio import qtgui

class UHD_B200_fosphor_rev2(gr.top_block, Qt.QWidget):

    def __init__(self, gain=0, span=40e6):
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

        self.settings = Qt.QSettings("GNU Radio", "UHD_B200_fosphor_rev2")

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
        self.span = span

        ##################################################
        # Variables
        ##################################################
        self.samp = samp = 40e6
        self.freq = freq = 444e6
        self.antenna = antenna = "RX2"

        ##################################################
        # Blocks
        ##################################################
        self.uhd_usrp_source_0_0 = uhd.usrp_source(
            ",".join(("", "")),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,1)),
            ),
        )
        self.uhd_usrp_source_0_0.set_center_freq(freq, 0)
        self.uhd_usrp_source_0_0.set_gain(gain, 0)
        self.uhd_usrp_source_0_0.set_antenna('RX2', 0)
        self.uhd_usrp_source_0_0.set_samp_rate(samp)
        self.uhd_usrp_source_0_0.set_time_unknown_pps(uhd.time_spec())
        self.fosphor_qt_sink_c_0_0_0 = fosphor.qt_sink_c()
        self.fosphor_qt_sink_c_0_0_0.set_fft_window(window.WIN_BLACKMAN_hARRIS)
        self.fosphor_qt_sink_c_0_0_0.set_frequency_range(freq, span)
        self._fosphor_qt_sink_c_0_0_0_win = sip.wrapinstance(self.fosphor_qt_sink_c_0_0_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._fosphor_qt_sink_c_0_0_0_win)
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
        self.connect((self.uhd_usrp_source_0_0, 0), (self.fosphor_qt_sink_c_0_0_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "UHD_B200_fosphor_rev2")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain
        self.uhd_usrp_source_0_0.set_gain(self.gain, 0)

    def get_span(self):
        return self.span

    def set_span(self, span):
        self.span = span
        self.fosphor_qt_sink_c_0_0_0.set_frequency_range(self.freq, self.span)

    def get_samp(self):
        return self.samp

    def set_samp(self, samp):
        self.samp = samp
        self.uhd_usrp_source_0_0.set_samp_rate(self.samp)

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.fosphor_qt_sink_c_0_0_0.set_frequency_range(self.freq, self.span)
        self.uhd_usrp_source_0_0.set_center_freq(self.freq, 0)

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
    parser.add_argument(
        "--span", dest="span", type=eng_float, default="40.0M",
        help="Set span [default=%(default)r]")
    return parser


def main(top_block_cls=UHD_B200_fosphor_rev2, options=None):
    if options is None:
        options = argument_parser().parse_args()

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls(gain=options.gain, span=options.span)

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
