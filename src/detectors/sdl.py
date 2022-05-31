# Detects if a game uses SDL
import os
import glob


def detect(path):
    if any(os.path.isfile(xp3) for xp3 in glob.iglob(os.path.join(path, 'SDL2.dll'), recursive=True)):
        return 'SDL2'

    if any(os.path.isfile(xp3) for xp3 in glob.iglob(os.path.join(path, 'SDL.dll'), recursive=True)):
        return 'SDL'
