#!/usr/bin/env python3
import os
import sys
import stat
import shutil
from distutils.core import setup


MODULE_ONLY = False
EMULATOR_EXEC = "/usr/local/bin/run-pifacedigital-emulator"


def install_executable():
    print("Installing executable.")
    shutil.copyfile("bin/run-pifacedigital-emulator", EMULATOR_EXEC)
    os.chmod(
        EMULATOR_EXEC,
        stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR |
        stat.S_IRGRP | stat.S_IXGRP |
        stat.S_IROTH | stat.S_IXOTH)


if "install" in sys.argv and not MODULE_ONLY:
    install_executable()


setup(
    name='pifacedigital_emulator',
    version='1.2',
    description='The PiFace Digital Emulator.',
    author='Thomas Preston',
    author_email='thomasmarkpreston@gmail.com',
    license='GPLv3+',
    url='https://github.com/piface/pifacedigital_emulator',
    packages=['pifacedigital_emulator'],
    classifiers=[
        "License :: OSI Approved :: GNU Affero General Public License v3 or "
        "later (AGPLv3+)",
        "Programming Language :: Python :: 3",
        "Development Status :: 5 - Production/Stable",
    ],
    keywords='piface digital emulator raspberrypi openlx',
)
