pifacedigital-emulator
======================

An emulator for the PiFace Digital I/O board.

Install
=======

Make sure you are using the lastest version of Raspbian::

    $ sudo apt-get update
    $ sudo apt-get upgrade

Install `pifacedigital-emulator` (for Python 3 and 2) with the following command::

    $ sudo apt-get install python3-pifacedigital-emulator


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
