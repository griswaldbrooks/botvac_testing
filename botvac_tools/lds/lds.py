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

# @file lds.py Module for processing the output of a Neato Botvac LDS.

import numpy as np


class Scan(object):
    """
    Class to hold one scan from the LDS.

    """
    def __init__(self):
        # Scan data.
        self._distances = np.array([], dtype=np.float32)
        self._angles = np.array([], dtype=np.float32)
        self._intensities = np.array([], dtype=np.int32)
        self._error_codes = np.array([], dtype=np.int32)

        # Dirty flag.
        self._unsorted = True
        # The max range for the Botvac LDS.
        # TODO: Should be configurable.
        self._distance_max = 5.

    def _sort_measurements(self):
        """
        Method to sort all of the measurements by angle.
        """
        if self._unsorted:
            sorted_ndxs = np.argsort(self._angles)
            self._distances = self._distances[sorted_ndxs]
            self._angles = self._angles[sorted_ndxs]
            self._intensities = self._intensities[sorted_ndxs]
            self._error_codes = self._error_codes[sorted_ndxs]
            self._unsorted = False

    def distances(self):
        """
        Method to return the distance measurements in meters.

        Returns:
            np.array: Distance measurements.
        """
        self._sort_measurements()
        return self._distances

    def angles(self):
        """
        Method to return the measurement angles in radians.

        Returns:
            np.array: Measurement angles.
        """
        self._sort_measurements()
        return self._angles

    def intensities(self):
        """
        Method to return the measurements intensities.

        Returns:
            np.array: Measurement intensities.
        """
        self._sort_measurements()
        return self._intensities

    def error_codes(self):
        """
        Method to return the measurement error codes.

        Returns:
            np.array: Measurement error codes.
        """
        self._sort_measurements()
        return self._error_codes

    def x(self):
        """
        Method to get the X coordinates of the 2D point cloud.

        Returns:
            np.array: 1D array of points.
                      The order of the points is sorted by angle.
        """
        self._sort_measurements()
        return self._distances*np.cos(self._angles)

    def y(self):
        """
        Method to get the Y coordinates of the 2D point cloud.

        Returns:
            np.array: 1D array of points.
                      The order of the points is sorted by angle.
        """
        self._sort_measurements()
        return self._distances*np.sin(self._angles)

    def points(self):
        """
        Method to get the 2D point cloud in cartesian coordinates.

        Returns:
            np.array: 2D array of points whose np.shape() = (2, n)
                      The first row contains all of the x coordinates.
                      The second row contains all of the y coordinates.
                      The order of the points is sorted by angle.
        """
        return np.vstack((self.x(), self.y()))

    def add_measurement(self,
                        distance,
                        angle,
                        intensity=0,
                        error_code=0,
                        linear_unit='millimeters',
                        angular_unit='degrees'):
        """
        Method to add a new measurement to the scan.

        Args:
            distance (float): Distance measured.
            angle (float): Angle at which the measurement was taken.
            intensity (int): Intensity of the reading.
            error_code  (int): Error code for the reading.
            linear_unit (str): Unit of the distance measurement.
                               Default is millimeters.
                               Available options are:
                                   millimeters
                                   meters
            angular_unit (str): Unit of the angle. Default is degrees.
                                Available options are:
                                    degrees
                                    radians
        """
        self._unsorted = True

        acceptable_lu = ['meters', 'millimeters']
        acceptable_au = ['degrees', 'radians']

        if linear_unit not in acceptable_lu:
            raise ValueError('{0} is not an available linear unit.'
                             .format(linear_unit))
        elif angular_unit not in acceptable_au:
            raise ValueError('{0} is not an available angular unit.'
                             .format(angular_unit))

        if linear_unit == 'millimeters':
            distance = distance/1000.

        if distance > self._distance_max:
            distance = 0

        if angular_unit == 'degrees':
            angle = angle*np.pi/180.

        self._distances = np.append(self._distances, distance)
        self._angles = np.append(self._angles, angle)
        self._intensities = np.append(self._intensities, intensity)
        self._error_codes = np.append(self._error_codes, error_code)
