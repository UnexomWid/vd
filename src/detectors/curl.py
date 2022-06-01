# Detects if a game uses curl
import os
import glob


def detect(path):
    if any(os.path.isfile(dll) for dll in glob.iglob(os.path.join(path, '**/libcurl.dll'), recursive=True)):
        return 'curl'
