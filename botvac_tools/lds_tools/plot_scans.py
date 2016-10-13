#!/usr/bin/env python
#
# MIT License
#
# Copyright (c) 2016 Griswald Brooks
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

#
# @author Griswald Brooks

# @file plot_scans.py Tool for displaying Neato Botvac LDS scans.

import argparse
import matplotlib.pyplot as plt
import numpy as np
import sys
from lds_tools import ScanParser


class ScanPlotter(object):
    """
    Class to display Neato Botvac LDS scans.
    """
    axis_margin = 0.1

    def __init__(self, scans):
        # LDS Scans.
        self._scans = scans
        self._xall = np.concatenate([scan.x() for scan in scans], axis=0)
        self._yall = np.concatenate([scan.y() for scan in scans], axis=0)
        self._xmax = max(self._xall)
        self._xmin = min(self._xall)
        self._ymax = max(self._yall)
        self._ymin = min(self._yall)
        # Index of the current scan.
        self._sdx = 0
        # Attach keyboard control callback to plotting objects.
        self._fig = plt.figure()
        self._ax = plt.subplot(111, aspect='equal')
        self._fig.canvas.mpl_connect('key_press_event', self._keyboard_control)
        self._ax.set_xlim(self._xmin - ScanPlotter.axis_margin,
                          self._xmax + ScanPlotter.axis_margin)
        self._ax.set_ylim(self._ymin - ScanPlotter.axis_margin,
                          self._ymax + ScanPlotter.axis_margin)

    def _replot(self):
        """
        Method to update the plot.
        """
        if 0 <= self._sdx < len(self._scans):
            # Get the current axes to use afterwards.
            xlim = self._ax.get_xlim()
            ylim = self._ax.get_ylim()

            # Grab new scan and plot it.
            scan = self._scans[self._sdx]
            self._ax.clear()
            self._ax.scatter(scan.x(),
                             scan.y(),
                             c=scan.intensities(),
                             cmap=plt.cm.brg)

            # Restore plot limits.
            self._ax.set_xlim(xlim)
            self._ax.set_ylim(ylim)
            self._fig.show()

    def _keyboard_control(self, event):
        """
        Method to change which frame is displayed or to exit.

        Args:
            event: Object holding key event presses.
        """
        sys.stdout.flush()
        # Go to the next frame.
        if event.key == 'd':
            self._sdx += 1

        # Go to the previous frame.
        elif event.key == 'a':
            self._sdx -= 1

        # Limit index.
        if self._sdx < 0:
            self._sdx = 0
        elif self._sdx >= len(self._scans):
            self._sdx = len(self._scans) - 1

        print('Scan index = {0}'.format(self._sdx))
        self._replot()

    def show_scans(self):
        """
        Function to plot the scan data.

        """

        print('Scan index = {0}'.format(self._sdx))
        scan = self._scans[self._sdx]
        self._ax.scatter(scan.x(),
                         scan.y(),
                         c=scan.intensities(),
                         cmap=plt.cm.brg)
        plt.show()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('log_file', metavar='logfile-to-parse',
                        help='name of the log file to extract scan data.')
    args = parser.parse_args()

    # Extract the scans and write them out.
    if args.log_file:
        scans = ScanParser.from_file(args.log_file)
        print("Extracted " + str(len(scans)) + " scans.")
        plotter = ScanPlotter(scans)
        print("Press 'd' to go to the next scan.")
        print("Press 'a' to go to the previous scan.")
        plotter.show_scans()

if __name__ == '__main__':
    main()
