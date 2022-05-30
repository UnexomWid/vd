# Detects games made with GameMaker
import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], '..'))
from utils.pe import get_version_info


def dump(path):
    # Strategy:
    # - check if the exe version info has an InternalName entry,
    #   and if it starts with GameMaker
    #
    # - if not, check if GMXInput.dll exists (it's XInput but Game Maker compatible)

    exes = [file for file in os.listdir(path) if os.path.isfile(os.path.join(path, file)) and file.endswith('.exe')]

    for exe in exes:
        info = get_version_info(os.path.join(path, exe))

        if not info:
            continue

        if 'InternalName' in info and info['InternalName'].startswith('GameMaker'):
            return {
                'Engine': 'GameMaker'
            }

    if os.path.exists(os.path.join(path, 'GMXInput.dll')):
        return {
            'Engine': 'GameMaker'
        }
