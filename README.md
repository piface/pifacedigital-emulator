pifacedigital-emulator
======================

An emulator for the PiFace Digital board. Requires [pifacedigitalio](https://github.com/piface/pifacedigitalio) to be installed.

[Screenshot](https://raw.github.com/piface/pifacedigital-emulator/master/images/pifacedigital_emulator_screenshot.png)

I built the UI with
[qt4-designer](http://doc.qt.digia.com/4.0/qt4-designer.html).

Install
=======

Download, build and install:

    git clone https://github.com/piface/pifacedigital-emulator.git
    cd pifacedigital-emulator/

    bin/build_ui.sh

    sudo python3 setup.py install

Or just install straight from PyPI:

    sudo easy_install3 pifacedigital-emulator

Use
===
To run the emulator type:

    $ pifacedigital-emulator

To use it with Python (just like pifacedigitalio):

    $ python3
    >>> import pifacedigital_emulator as emu
    >>> emu.init() # a window should pop up
    >>> pifacedigital = emu.PiFaceDigital()
    >>> pifacedigital.leds[0].toggle()

See http://piface.github.io/pifacedigitalio/example.html
