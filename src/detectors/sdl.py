# Detects if a game uses SDL
import os
import glob


def detect(path):
    for dll in glob.iglob(os.path.join(path, '**/SDL[0-9]*.dll'), recursive=True):
        if os.path.isdir(dll):
            continue

        return os.path.basename(dll)[:-4]  # SDL + the version, if any
