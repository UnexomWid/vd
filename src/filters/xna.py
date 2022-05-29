# Detect games made with Microsoft XNA
import os


def dump(path):
    # Strategy:
    # - enumerate all exe files, since we don't know which exe is the game itself
    #   (should be solved in the future by passing the exe file)
    # - search for the 'Microsoft.Xna' string inside all executable files
    # - possible strategies for the future: check if *.xnb files exist

    # This only works for Windows exes
    exes = [file for file in os.listdir(path) if os.path.isfile(os.path.join(path, file)) and file.endswith('.exe')]

    for exe in exes:
        with open(os.path.join(path, exe), 'rb') as file:
            # Reading the whole file can take some time for large games
            # This is why the XNA filter has low priority
            data = file.read()

            if b'Microsoft.Xna' in data:
                return {
                    'Framework': 'Microsoft XNA'
                }
