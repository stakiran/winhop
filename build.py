# encoding: utf-8

import os
import sys

from cx_Freeze import setup, Executable

name        = 'winhop'
version     = '1.0.0'
description = 'winhop'
base        = 'Win32GUI'
icon_path   = 'app.ico'

# http://cx-freeze.readthedocs.io/en/latest/distutils.html#build-exe
outdir   = '{:}'.format(name)
includes = []
excludes = []
packages = []
options = {
    'build_exe': {
        'build_exe': outdir,
        'includes' : includes,
        'excludes' : excludes,
        'packages' : packages,
    },
}

# http://cx-freeze.readthedocs.io/en/latest/distutils.html#cx-freeze-executable
entrypoint_filename = 'winhop.py'
entrypoint_fullpath = entrypoint_filename
executables = [
    Executable(entrypoint_fullpath, base=base, icon=icon_path)
]

setup(
    name        = name,
    version     = version,
    description = description,
    options     = options,
    executables = executables
)
