# Detects games made with GlyphX
import os

def detect(path, exes, dlls):
    # Strategy:
    # - search for the 'GLYPHX' string inside exe files

    for exe in exes:
        with open(os.path.join(path, exe), 'rb') as file:
            data = file.read()

            if b'GLYPHX' in data:
                return {
                    'Engine': 'GlyphX'
                }
