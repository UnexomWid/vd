# Detects if a game uses Lua
import os
import glob


def detect(path):
    if any(os.path.isfile(dll) for dll in glob.iglob(os.path.join(path, '**/lua*.dll'), recursive=True)):
        return 'Lua'
