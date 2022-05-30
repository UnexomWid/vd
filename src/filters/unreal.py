# Detect games made with Unreal
import os
import glob


def dump(path):
    # Strategy:
    # - see if the game has a Binaries directory
    # - if it does, it's probably Unreal

    if any(os.path.isdir(bin) for bin in glob.iglob(os.path.join(path, 'Binaries'), recursive=True)):
        return {
            'Engine': 'Unreal'
        }
