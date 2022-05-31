# Detects if a game uses Tale
# https://github.com/deprimus/Tale
import os
import glob


def detect(path):
    if any(os.path.isfile(dll) for dll in glob.iglob(os.path.join(path, '**/Tale.dll'), recursive=True)):
        return 'Tale'
