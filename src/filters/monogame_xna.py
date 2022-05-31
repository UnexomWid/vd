# Detect games made with MonoGame or Microsoft XNA
import os


def dump(path):
    # Strategy:
    # - enumerate all exe files, since we don't know which exe is the game itself
    #   (should be solved in the future by passing the exe file)
    #
    # - search for the 'MonoGame' string inside the exe (or 'Microsoft.Xna')
    #
    # - if the exe doesn't have it, check for a DLL with the same name as the exe
    #   (some games have this DLL that contains the string, like Barotrauma)
    #
    # - if the DLL doesn't have it either, skip to the next exe

    exes = [file for file in os.listdir(path) if os.path.isfile(os.path.join(path, file)) and file.endswith('.exe')]

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
                    