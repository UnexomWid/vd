# Detects games made with OpenFL (formerly HaxeNME)
import os


def dump(path):
    # Strategy:
    # - enumerate all exe files
    # - search for the 'openfl' string inside the exe
    # - if it wasn't found, skip to the next exe

    exes = [file for file in os.listdir(path) if os.path.isfile(os.path.join(path, file)) and file.endswith('.exe')]

    for exe in exes:
        with open(os.path.join(path, exe), 'rb') as file:
            data = file.read()

            if b'openfl' in data:
                return {
                    'Engine': 'OpenFL'
                }