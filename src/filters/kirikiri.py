# Detects games made with KiriKiri/KAG
import os
import sys
import glob

sys.path.insert(1, os.path.join(sys.path[0], '..'))
from utils.pe import get_version_info


def dump(path):
    # Strategy:
    # - check the exe version info for interesting strings:
    #   - FileDescription: TVP(KIRIKIRI) 2 core... -> this is KiriKiri 2
    #   - ProductName: TVP(KIRIKIRI) Z core... -> this is KiriKiri Z
    #
    # - if nothing was found, check if there are any .xp3 files;
    #   if so, it's most likely KiriKiri

    exes = [file for file in os.listdir(path) if os.path.isfile(os.path.join(path, file)) and file.endswith('.exe')]

    for exe in exes:
        info = get_version_info(os.path.join(path, exe))

        if not info:
            continue

        if 'FileDescription' in info and info['FileDescription'].startswith('TVP(KIRIKIRI) 2'):
            return {
                'Engine': 'KiriKiri2/KAG3'
            }

        if 'ProductName' in info and info['ProductName'].startswith('TVP(KIRIKIRI) Z'):
            return {
                'Engine': 'KiriKiriZ/KAG3'
            }

    if any(os.path.isdir(xp3) for xp3 in glob.iglob(os.path.join(path, '*.xp3'), recursive=True)):
        return {
            'Engine': 'KiriKiri/KAG'
        }
