# Detects if a game uses ANTLR
# e.g. Higurashi When They Cry is made in Unity,
# but uses ANTLR to parse some scripts which contain the story itself
import os
import glob


def detect(path):
    for dll in glob.iglob(os.path.join(path, '**/Antlr[0-9]*.Runtime.dll'), recursive=True):
        if os.path.isdir(dll):
            continue

        return os.path.basename(dll)[:-12].upper()  # ANTLR + the version
