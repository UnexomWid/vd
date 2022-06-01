# Detects if a game uses Lidgren
import os
import glob


def detect(path):
    if any(os.path.isfile(dll) for dll in glob.iglob(os.path.join(path, '**/Lidgren*.dll'), recursive=True)):
        return 'Lidgren'
