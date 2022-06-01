# Detects games made with RealLive or Siglus
import os
import sys
import glob

sys.path.insert(1, os.path.join(sys.path[0], '..'))
from utils.pe import get_version_info

def dump(path):
    # Strategy:
    # - check the exe version info for interesting strings:
    #   - FileDescription: RealLive Engine
    #
    # - if such a string exists, check if there's a file that starts with Siglus
    #   - if there is, it's probably Siglus; otherwise, it's probably RealLive

    exes = [file for file in os.listdir(path) if os.path.isfile(os.path.join(path, file)) and file.endswith('.exe')]

    for exe in exes:
        info = get_version_info(os.path.join(path, exe))

        if not info:
            continue

        if 'FileDescription' in info and 'RealLive' in info['FileDescription']:
            if any(glob.iglob(os.path.join(path, '**/Siglus*'))):
                return {
                    'Engine': 'Siglus'
                }

            return {
                'Engine': 'RealLive'
            }
