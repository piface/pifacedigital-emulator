#!/usr/bin/env python3
from distutils.core import setup, Extension

DISTUTILS_DEBUG=True

setup(name='pifacedigital-emulator',
	version='1.0',
	description='The PiFace Digital Emulator.',
	author='Thomas Preston',
	author_email='thomasmarkpreston@gmail.com',
	license='GPLv3+',
	url='http://pi.cs.man.ac.uk/interface.htm',
	py_modules=['pifacedigital_emulator',
        'pfemgui',
        'pifacedigital_emulator_ui',
        'pifacedigital_emulator_rc',
        ],
)
