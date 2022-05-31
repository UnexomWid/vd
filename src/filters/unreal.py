# Detect games made with Unreal
import os
import sys
import glob

sys.path.insert(1, os.path.join(sys.path[0], '..'))
from utils.pe import get_version_info


def dump(path):
    # Strategy:
    # - check the exe version info for interesting strings
    #   - InternalName: UnrealEngine
    #   - ProductVersion: this has the engine version
    #
    # - if nothing is found, see if the game has either an UDKGame or Binaries directory;
    #   if it does, it's probably Unreal

    exes = [file for file in os.listdir(path) if os.path.isfile(os.path.join(path, file)) and file.endswith('.exe')]

    for exe in exes:
        info = get_version_info(os.path.join(path, exe))

        if not info:
            continue

        if 'InternalName' in info and info['InternalName'] == 'UnrealEngine':
            if 'ProductVersion' in info and len(info['ProductVersion'].strip()) > 0:
                return {
                    'Engine': f"Unreal ({info['ProductVersion'].strip()})"
                }
            return {
                'Engine': 'Unreal'
            }

    if any(os.path.isdir(bin) for bin in glob.iglob(os.path.join(path, 'UDKGame'), recursive=True)):
        return {
            'Engine': 'Unreal'
        }

    if any(os.path.isdir(bin) for bin in glob.iglob(os.path.join(path, 'Binaries'), recursive=True)):
        return {
            'Engine': 'Unreal'
        }
