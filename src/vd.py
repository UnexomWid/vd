import sys
import os
import glob

import engines.unity
import engines.renpy
import engines.gamemaker
import engines.nscripter
import engines.kirikiri
import engines.real_live
import engines.ethornell
import engines.monogame_xna
import engines.unreal
import engines.openfl
import engines.glyphx
import engines.unknown

import detectors.dll

from utils.misc import dict_append_list


# Dumps info about a game located in a path,
# based on a list of engine and library detectors
def dump(path, engines, detectors):
    result = {}

    # List all exe and dll files and pass them to the engine and library detectors
    exes = glob.glob(os.path.join(path, '**/*.exe'), recursive=True)
    dlls = glob.glob(os.path.join(path, '**/*.dll'), recursive=True)

    # TODO: try except
    for engine in engines:
        engine_result = engine(path, exes, dlls)

        if engine_result is not None:
            result = engine_result  # Engine detected
            break

    # Library detectors require the DLL basenames
    dll_basenames = set(map(lambda x: os.path.basename(x), dlls))

    for detector in detectors:
        detection = detector(path, exes, dll_basenames)

        if detection is not None:
            for entry in detection:
                dict_append_list(result, 'Detected', entry)

    return result


def main():
    if len(sys.argv) == 1:
        sys.argv.append(os.getcwd())

    engine_list = [
        engines.unity.detect,
        engines.renpy.detect,
        engines.kirikiri.detect,
        engines.real_live.detect,
        engines.gamemaker.detect,
        engines.nscripter.detect,
        engines.ethornell.detect,
        engines.monogame_xna.detect,
        engines.unreal.detect,
        engines.openfl.detect,
        engines.glyphx.detect,
        engines.unknown.detect
    ]

    detector_list = [
        detectors.dll.detect
    ]

    sys.argv = sys.argv[1:]  # Remove script path

    for dir in sys.argv:
        print(f'Game: {os.path.basename(dir)}')
        data = dump(dir, engine_list, detector_list)

        for key, value in data.items():
            print(f'{key}: {value}')

        print()


if __name__ == '__main__':
    main()