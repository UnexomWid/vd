# Detects games made with GameMaker
# e.g. Touhou Luna Nights uses GameMaker, but they call it Mogura Engine 2 (which could be a GameMaker template?)
import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], '..'))
from utils.pe import get_version_info


def detect(path, exes, dlls):
    # Strategy:
    # - check if the exe version info has an InternalName entry,
    #   and if it starts with GameMaker
    #
    # - if not, check if GMXInput.dll exists (it's XInput but Game Maker compatible)
    # - if that doesn't exist, check for data.win (it's common among Game Maker games)

    for exe in exes:
        info = get_version_info(os.path.join(path, exe))

        if not info:
            continue

        if 'InternalName' in info and info['InternalName'].startswith('GameMaker'):
            return {
                'Engine': 'GameMaker'
            }

    if any(filter(lambda x: x.endswith('GMXInput.dll'), dlls)):
        return {
            'Engine': 'GameMaker'
        }

    if os.path.exists(os.path.join(path, 'data.win')):
        return {
            'Engine': 'GameMaker'
        }
