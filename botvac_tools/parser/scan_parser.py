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

# @file scan_parser.py Module for parsing Neato Botvac LDS scan data.

from ..lds import Scan


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
