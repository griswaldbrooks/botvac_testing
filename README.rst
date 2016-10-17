.. image:: https://travis-ci.org/griswaldbrooks/botvac_tools.svg?branch=master
    :target: https://travis-ci.org/griswaldbrooks/botvac_tools
============
Botvac Tools
============
Repo to hold scripts and instructions for testing the Neato Robotics Botvac.

Getting Started
===============
- `Testing Commands <docs/testing.md>`_
- `Plot Scan <docs/plot_scan.md>`_

Drivers
=======
To connect to the robot via the USB port, you may need to install
a device driver.

Linux
-----
Ubuntu 14.04 and 16.04 do not need special drivers to communicate with the
robot. It will appear as a serial port, such as `/dev/ttyACM0`

Windows
-------
Windows 7 and 10 require driver installation to communicate with the robot.

- 32-bit:
    `NeatoUpdaterToolInstaller_x86 <http://www.neatoroboticsupdates.com/NeatoInstaller/NeatoUpdaterToolInstaller_x86.exe>`_
- 64-bit:
    `NeatoUpdaterToolInstaller_x64 <http://www.neatoroboticsupdates.com/NeatoInstaller/NeatoUpdaterToolInstaller_x64.exe>`_

The robot will then show up as a COM port, which you can connect to using a
program such as `TeraTerm <https://ttssh2.osdn.jp/index.html.en>`_ 
or `Putty <http://www.putty.org/>`_.
