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

# @file lds_tools.py Module for processing the output of a Neato Botvac LDS.

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


class ScanParser(object):
    """
    Class for creating Scan objects from strings and files.
    """
    @staticmethod
    def file_to_strings(filename):
        """
        Function to create a list of strings. Each string contains the data
        from one LDS scan.

        Args:
            filename (str): Name of the file containing the laser scan(s).

        Returns:
            list: List of scan strings.
        """
        # Scan output list.
        scans = list()
        scan_string = str()

        # Parsing tokens.
        # TODO: Allow changing of tokens.
        start_token = 'AngleInDegrees'
        end_token = 'ROTATION_SPEED'
        # Parsing flags.
        append_to_str = False

        # Parse file into scan strings.
        with open(filename, 'rb') as scan_file:
            for line in scan_file:
                if start_token in line:
                    # If we hit the start token, start recording a new string.
                    scan_string = str()
                    append_to_str = True
                elif end_token in line and append_to_str:
                    # If we hit the end token and we were recording then save.
                    scans.append(scan_string)
                    append_to_str = False
                elif append_to_str:
                    scan_string += line

        return scans

    @staticmethod
    def from_string(scan_string):
        """
        Function to parse an LDS scan string into.

        Args:
            scan_string (str): String containing the laser scan.

        Returns:
            Scan: The parsed Scan object.
        """
        scan_lines = scan_string.split()
        scan = Scan()
        prev_angle = 'No previous angle.'

        for line in scan_lines:
            meas = line.split(',')
            # If the measurement doesn't have the right number of elements
            # something went wrong.
            if len(meas) != 4:
                raise ValueError('{0} could not be parsed.'.format(line))

            angle = float(meas[0])
            distance = float(meas[1])
            intense = int(meas[2])
            err = int(meas[3])

            # All of the elements should be positive.
            if distance < 0:
                raise ValueError('{0} is an invalid distance.'
                                 .format(distance))
            if angle < 0 or angle > 359:
                raise ValueError('{0} is an invalid angle.'.format(angle))
            if intense < 0:
                raise ValueError('{0} is an invalid intensity.'
                                 .format(intense))
            if err < 0:
                raise ValueError('{0} is an invalid error code.'.format(err))

            # The angles should always increase in value.
            if prev_angle == 'No previous angle.':
                prev_angle = angle
            elif prev_angle >= angle:
                raise ValueError(('{0} was not an increase from the previous'
                                  ' angle of {1}.').format(angle, prev_angle))

            scan.add_measurement(distance, angle, intense, err)

        return scan

    @classmethod
    def from_file(cls, filename):
        """
        Function to produce scan objects from LDS scans in a file.

        Args:
            filename (str): Name of the file with scans.

        Returns:
            list: List of Scan objects.
        """
        scans = list()
        scan_strings = cls.file_to_strings(filename)
        for scan_string in scan_strings:
            try:
                scans.append(cls.from_string(scan_string))
            except Exception:
                pass

        return scans
