# Detect games made with Unreal
import os
import glob


def dump(path):
    # Strategy:
    # - see if the game has a Binaries directory
    # - if it does, it's probably Unreal

    bins = [bin for bin in glob.glob(os.path.join(path, 'Binaries'), recursive=True) if os.path.isdir(bin)]

    if len(bins) > 0:
        return {
            'Engine': 'Unreal'
        }
