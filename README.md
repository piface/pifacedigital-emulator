pifacedigital-emulator
======================

An emulator for the PiFace Digital board. Requires [pifacedigitalio](https://github.com/piface/pifacedigitalio) to be installed.

[Screenshot](https://raw.github.com/piface/pifacedigital-emulator/master/images/pifacedigital_emulator_screenshot.png)

Installation
============

$ sudo ./install.sh

Usage
=====
To run the emulator type:

    $ pifacedigital-emulator

To use it with Python (just like pifacedigitalio):

    $ python3
    >>> import pifacedigital_emulator as emu
    >>> emu.init() # a window should pop up
    >>> emu.PiFaceDigital().leds[0].toggle()

See https://github.com/piface/pifacedigitalio#examples.

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

    gpio-admin: could not flush data to /sys/class/gpio/export: Device or resource busy

A. This is probably because the emulator was exited incorrectly. Run this:

    $ gpio-admin unexport 25
