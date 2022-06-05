# Detects games made with OpenFL (formerly HaxeNME)
import os


def detect(path, exes, dlls):
    # Strategy:
    # - search for the 'openfl' string inside exe files

    for exe in exes:
        with open(os.path.join(path, exe), 'rb') as file:
            data = file.read()

            if b'openfl' in data:
                return {
                    'Engine': 'OpenFL'
                }