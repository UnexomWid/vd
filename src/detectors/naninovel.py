# Detects if a game uses Naninovel
# https://naninovel.com/
import os
import glob


def detect(path):
    if any(os.path.isfile(dll) for dll in glob.iglob(os.path.join(path, '**/Naninovel*.dll'), recursive=True)):
        return 'Naninovel'
