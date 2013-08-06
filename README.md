pifacedigital-emulator
======================

An emulator for the PiFace Digital I/O board.

Install
=======

Download the latest debian package from
[here](https://github.com/piface/pifacedigital-emulator/releases) and install with:

    $ dpkg -i python3-pifacedigital-emulator_1.2.0-1_all.deb

You may also need to install the latest releases of
[pifacedigitalio](https://github.com/piface/pifacedigitalio/releases) and
[pifacecommon](https://github.com/piface/pifacecommon/releases).

Or you can install without using your package manager:

    $ git clone https://github.com/piface/pifacedigitalio.git
    $ cd pifacedigitalio
    $ bin/build_ui.sh
    $ sudo python3 setup.py install

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
