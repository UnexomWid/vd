# Detects games made with RealLive/Siglus
import os
import sys
import glob

sys.path.insert(1, os.path.join(sys.path[0], '..'))
from utils.pe import get_version_info

def detect(path, exes, dlls):
    # Strategy:
    # - check the exe version info for interesting strings:
    #   - FileDescription: RealLive Engine
    #
    # - if such a string exists, check if there's a file that starts with Siglus
    #   - if there is, it's probably Siglus; otherwise, it's probably RealLive

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
