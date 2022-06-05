# Detect games made with MonoGame or Microsoft XNA
import os


def detect(path, exes, dlls):
    # Strategy:
    # - search for the 'MonoGame' (or 'Microsoft.Xna') string inside exe files
    #
    # - if no exes have it, check for a DLLs named after the exes
    #   (some games like Barotrauma have DLLs named after the exes that contain the string)

    for exe in exes:
        with open(os.path.join(path, exe), 'rb') as file:
            data = file.read()

            if b'MonoGame' in data:
                return {
                    'Framework': 'MonoGame'
                }
            if b'Microsoft.Xna' in data:
                return {
                    'Framework': 'Microsoft XNA'
                }

            dll = os.path.join(path, exe)[:-3] + 'dll'

            if os.path.exists(dll):
                with open(dll, 'rb') as dll_file:
                    dll_data = dll_file.read()

                    if b'MonoGame' in dll_data:
                        return {
                            'Framework': 'MonoGame'
                        }
                    if b'Microsoft.Xna' in dll_data:
                        return {
                            'Framework': 'Microsoft XNA'
                        }
                    