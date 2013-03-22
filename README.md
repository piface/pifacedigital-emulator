pifacedigital-emulator
======================

An emulator for the PiFace Digital board.

WORK IN PROGRESS

Development notes
================
You need to generate the resource and UI python files using the following
command:

    $ pyside-rcc pifacedigital_emulator.qrc -o pifacedigital_emulator_rc.py -py3
    $ pyside-uic pifacedigital_emulator.ui -o pifacedigital_emulator_ui.py
