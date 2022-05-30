# Detect games made with NScripter, ONScripter or Ponscripter

import os
import sys

# Ugly, but whatever. Since python absolutely refuses to work
# with sibling directories (even with __init__.py), I have to do this manually.
# Restructuring the project isn't an option because:
# - it's fine the way it is
# - the utils directory contains, well, utils used by all scripts
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from utils.pe import get_version_info


def dump(path):
    # Strategy:
    # - if pscript.dat exists, it's most likely Ponscripter
    #
    # - check the exe version info for interesting strings: ProductName -> Ponscripter
    #
    # - at least one of the following files should exist:
    #   nscript.dat, 0.txt, arc.nsa
    #   (nscript.dat seems to be a compiled version of 0.txt?)
    #
    # - if default.ttf exists, along with at least one file listed previously,
    #   then it's most likely ONScripter since it requires that font to exist

    if os.path.exists(os.path.join(path, 'pscript.dat')):
        return {
            'Engine': 'Ponscripter'
        }

    # This only works for Windows exes
    exes = [file for file in os.listdir(path) if os.path.isfile(os.path.join(path, file)) and file.endswith('.exe')]

    for exe in exes:
        info = get_version_info(os.path.join(path, exe))

        if not info:
            continue

        if 'ProductName' in info and info['ProductName'] == 'Ponscripter':
            return {
                'Engine': 'Ponscripter'
            }

    required = ['nscript.dat', '0.txt', 'arc.nsa']
    has_required = any(os.path.exists(os.path.join(path, file)) for file in required)

    if has_required:
        if os.path.exists(os.path.join(path, 'default.ttf')):
            return {
                'Engine': 'ONScripter'
            }

        return {
            'Engine': 'NScripter'
        }
