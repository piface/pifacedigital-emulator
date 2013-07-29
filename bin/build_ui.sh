#!/bin/bash
#: Description: builds the ui for pifacedigital_emulator

rcsource="src/pifacedigital_emulator.qrc"
rcfile="pifacedigital_emulator/pifacedigital_emulator_rc.py"
uisource="src/pifacedigital_emulator.ui"
uifile="pifacedigital_emulator/pifacedigital_emulator_ui.py"

printf "Generating resource.\n"
pyside-rcc $rcsource -o $rcfile -py3
printf "Generating UI.\n"
pyside-uic $uisource -o $uifile

# pyside doesn't know about Python submodules
printf "Fixing UI.\n"
string="import pifacedigital_emulator_rc"
replace="import pifacedigital_emulator.pifacedigital_emulator_rc"
sed -e "s/$string/$replace/" $uifile >> /tmp/pifacedigital_emulator_ui_file
mv /tmp/pifacedigital_emulator_ui_file $uifile