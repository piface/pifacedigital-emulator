#!/bin/bash
#: Description: Installs pifacedigitalio-emulator and its dependecies

# check if the script is being run as root
if [[ $EUID -ne 0 ]]
then
    printf 'This script must be run as root.\nExiting..\n'
    exit 1
fi

# depends on pifacedigitalio
python3 -c "import pifacedigitalio" # is it installed?
if [ $? -ne 0 ]
then
    # install pifacecommon
    printf "Downloading pifacedigitalio...\n"
    git clone https://github.com/piface/pifacedigitalio.git
    cd pifacedigitalio
    ./install.sh
    cd -
    printf "\n"
fi

# more dependencies (aptitude is too slow)
apt-get install python3-pyside pyside-tools

printf "Installing pifacedigitalio-emulator...\n"
pyside-uic pifacedigital_emulator.ui -o pifacedigital_emulator_ui.py && \
pyside-rcc pifacedigital_emulator.qrc -o pifacedigital_emulator_rc.py -py3 && \
python3 setup.py install
printf "Done!\n"
