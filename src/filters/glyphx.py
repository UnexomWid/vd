# Detects games made with GlyphX
import os

def dump(path):
    # Strategy:
    # - enumerate all exe files
    # - search for the 'GLYPHX' string inside the exe

    exes = [file for file in os.listdir(path) if os.path.isfile(os.path.join(path, file)) and file.endswith('.exe')]

    for exe in exes:
        with open(os.path.join(path, exe), 'rb') as file:
            data = file.read()

            if b'GLYPHX' in data:
                return {
                    'Engine': 'GlyphX'
                }
