pifacedigital-emulator
======================

An emulator for the PiFace Digital I/O board.

Install
=======

First, install python-pyside:

    $ sudo apt-get install python{,3}-pyside

Then download and install (using `dpkg`, see below) the latest releases of:
- [pifacecommon](https://github.com/piface/pifacecommon/releases)
- [pifacedigitalio](https://github.com/piface/pifacedigitalio/releases)

Finally, download the latest release of [pifacedigital-emulator](https://github.com/piface/pifacedigital-emulator/releases) and install with:

    $ sudo dpkg -i python3-pifacedigital-emulator_1.2.0-1_all.deb


Use
===
To run the emulator type:

    $ pifacedigital-emulator

To use it with Python (just like
[pifacedigitalio](https://github.com/piface/pifacedigitalio)):

    $ python3
    >>> import pifacedigital_emulator as emu
    >>> emu.init()  # a window should pop up
    >>> pifacedigital = emu.PiFaceDigital()
    >>> pifacedigital.leds[0].toggle()

See http://piface.github.io/pifacedigitalio/example.html


Development Notes
=================
UI built with [qt4-designer](http://doc.qt.digia.com/4.0/qt4-designer.html).
To generate the UI files, run:

    bin/build_ui.sh
