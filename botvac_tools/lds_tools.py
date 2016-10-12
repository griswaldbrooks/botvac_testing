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
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

##
# @author Griswald Brooks

## @file lds_tools.py Script for plotting the outputof an LDS scan.

import matplotlib.pyplot as plt
import numpy as np

def parse_scan_file(filename):
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
    start_token = 'AngleInDegrees'
    end_token = 'ROTATION_SPEED'

    # Parse file into scan strings.
    with open(filename, 'rb') as scan_file:
        for line in scan_file:
            if start_token in line:
                scan_string += line

    return scans

def parse_scan(scan_str):
    """
    Function to parse an LDS scan from the command line interface.

    Args:
        filename (str): Name of the file containing the laser scan.

    Returns:
        list: List of scan objects.
    """
    # Tokens for scan segment.
    start_token = "LDS Readings for SvcBaseManagement"
    end_token = "iBrightestReading"

    # Scan records to be written.
    records = []

    with open(filename, "rb") as f:
        for line in f:
            scan = Scan()
            if start_token in line:
                sys.stdout.write(".")
                sys.stdout.flush()
                line = next(f)
                # Read in the scan data.
                while end_token not in line:
                    try:
                        scan.add_point_from_line(line)
                    except:
                        sys.stdout.write(",")
                        sys.stdout.flush()
                    line = next(f)

            # Add it to the records.
            if scan.size():
                records.append(scan)

    return records

