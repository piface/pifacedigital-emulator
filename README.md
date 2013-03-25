pifacedigital-emulator
======================

An emulator for the PiFace Digital board.

[Screenshot](https://raw.github.com/piface/pifacedigital-emulator/master/images/pifacedigital_emulator_screenshot.png)

Installation
============
Dependencies
------------
First, install pyside and pyside-tools:

    $ sudo apt-get install python3-pyside pyside-tools

Generate the resource and UI files:

    $ pyside-uic pifacedigital_emulator.ui -o pifacedigital_emulator_ui.py
    $ pyside-rcc pifacedigital_emulator.qrc -o pifacedigital_emulator_rc.py -py3

Install with Python:

    $ sudo python3 setup.py install

Copy the emulator runner script and set its permissions:

    $ sudo cp run-pifacedigital-emulator /usr/local/bin/pifacedigital-emulator
    $ sudo chmod a+x /usr/local/bin/pifacedigital-emulator

Usage
=====
To run the emulator type:

    $ pifacedigital-emulator

To use it with Python (just like pifacedigitalio):

    $ python3
    >>> import pifacedigital_emulator as emu
    >>> emu.init() # a window should pop up
    >>> emu.write(0xAA, emu.OUTPUT_PORT)

Development notes
=================
You need to generate the resource and UI python files using the following
commands:

    $ pyside-rcc pifacedigital_emulator.qrc -o pifacedigital_emulator_rc.py -py3
    $ pyside-uic pifacedigital_emulator.ui -o pifacedigital_emulator_ui.py

I generated the UI with
[qt4-designer](http://doc.qt.digia.com/4.0/qt4-designer.html).

F.A.Q.
======
Q. I keep getting the following error:

    gpio-admin: could not flush data to /sys/class/gpio/export: Device or
    resource busy

A. This is probably because the emulator was exited incorrectly. Run this:

    $ gpio-admin unexport 25
