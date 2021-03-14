#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: UHF Band
# Author: David Badger
# Description: ISM Band capture
# GNU Radio version: 3.8.2.0

from gnuradio import blocks
from gnuradio import gr
from gnuradio.filter import firdes
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import uhd
import time
import gr_sigmf


class record_live1msps(gr.top_block):

    def __init__(self, antenna="RX2", args="", filename="", freq=433.65e6, gain=0, samp_rate=1e6, seconds=10, subdev=""):
        gr.top_block.__init__(self, "UHF Band")

        ##################################################
        # Parameters
        ##################################################
        self.antenna = antenna
        self.args = args
        self.filename = filename
        self.freq = freq
        self.gain = gain
        self.samp_rate = samp_rate
        self.seconds = seconds
        self.subdev = subdev

        ##################################################
        # Blocks
        ##################################################
        self.uhd_usrp_source_0 = uhd.usrp_source(
            ",".join(("", args)),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,1)),
            ),
        )
        self.uhd_usrp_source_0.set_center_freq(freq, 0)
        self.uhd_usrp_source_0.set_gain(gain, 0)
        self.uhd_usrp_source_0.set_antenna(antenna, 0)
        self.uhd_usrp_source_0.set_bandwidth(samp_rate, 0)
        self.uhd_usrp_source_0.set_samp_rate(samp_rate)
        self.uhd_usrp_source_0.set_time_unknown_pps(uhd.time_spec())
        self.sigmf_sink_0 = gr_sigmf.sink("cf32", '/home/david/sigMF_ML/RF/ramdisk/test1', gr_sigmf.sigmf_time_mode_relative, False)
        self.sigmf_sink_0.set_global_meta("core:sample_rate", samp_rate)
        self.sigmf_sink_0.set_global_meta("core:description", 'Filtered')
        self.sigmf_sink_0.set_global_meta("core:author", 'David Badger')
        self.sigmf_sink_0.set_global_meta("core:license", '')
        self.sigmf_sink_0.set_global_meta("core:hw", 'N210')

        self.sigmf_sink_0.set_global_meta('core:hardware', 'noise')

        self.sigmf_sink_0.set_global_meta('core:BW', 'none')

        self.sigmf_sink_0.set_global_meta('core:SNR', 0)

        self.sigmf_sink_0.set_global_meta('core:modulation', 'none')

        self.sigmf_sink_0.set_global_meta('core:DTMF', 'NA')

        self.sigmf_sink_0.set_global_meta('core:class', '4')
        self.blocks_head_0 = blocks.head(gr.sizeof_gr_complex*1, int(samp_rate*seconds))



        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_head_0, 0), (self.sigmf_sink_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.blocks_head_0, 0))


    def get_antenna(self):
        return self.antenna

    def set_antenna(self, antenna):
        self.antenna = antenna
        self.uhd_usrp_source_0.set_antenna(self.antenna, 0)

    def get_args(self):
        return self.args

    def set_args(self, args):
        self.args = args

    def get_filename(self):
        return self.filename

    def set_filename(self, filename):
        self.filename = filename

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.uhd_usrp_source_0.set_center_freq(self.freq, 0)

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain
        self.uhd_usrp_source_0.set_gain(self.gain, 0)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_head_0.set_length(int(self.samp_rate*self.seconds))
        self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)
        self.uhd_usrp_source_0.set_bandwidth(self.samp_rate, 0)

    def get_seconds(self):
        return self.seconds

    def set_seconds(self, seconds):
        self.seconds = seconds
        self.blocks_head_0.set_length(int(self.samp_rate*self.seconds))

    def get_subdev(self):
        return self.subdev

    def set_subdev(self, subdev):
        self.subdev = subdev




def argument_parser():
    description = 'ISM Band capture'
    parser = ArgumentParser(description=description)
    parser.add_argument(
        "--freq", dest="freq", type=eng_float, default="433.65M",
        help="Set freq [default=%(default)r]")
    parser.add_argument(
        "--gain", dest="gain", type=eng_float, default="0.0",
        help="Set gain [default=%(default)r]")
    parser.add_argument(
        "--samp-rate", dest="samp_rate", type=eng_float, default="1.0M",
        help="Set samp_rate [default=%(default)r]")
    parser.add_argument(
        "--seconds", dest="seconds", type=eng_float, default="10.0",
        help="Set seconds [default=%(default)r]")
    return parser


def main(top_block_cls=record_live1msps, options=None):
    if options is None:
        options = argument_parser().parse_args()
    tb = top_block_cls(freq=options.freq, gain=options.gain, samp_rate=options.samp_rate, seconds=options.seconds)

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()

    tb.wait()


if __name__ == '__main__':
    main()
