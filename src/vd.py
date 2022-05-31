import sys
import os

import filters.unity
import filters.renpy
import filters.gamemaker
import filters.nscripter
import filters.kirikiri
import filters.ethornell
import filters.monogame_xna
import filters.unreal
import filters.openfl
import filters.glyphx
import filters.unknown

import detectors.sdl
import detectors.lua
import detectors.tale

from utils.misc import dict_append_list


def dump(path, filters, detectors):
    result = {}
    # TODO: try except
    for filter in filters:
        filter_result = filter(path)

        if filter_result is not None:
            result = filter_result
            break

    for detector in detectors:
        detection = detector(path)

        if detection is not None:
            dict_append_list(result, 'Detected', detection)

    return result


def main():
    if len(sys.argv) == 1:
        sys.argv.append(os.getcwd())

    filter_list = [
        filters.unity.dump,
        filters.renpy.dump,
        filters.kirikiri.dump,
        filters.gamemaker.dump,
        filters.nscripter.dump,
        filters.ethornell.dump,
        filters.monogame_xna.dump,
        filters.unreal.dump,
        filters.openfl.dump,
        filters.glyphx.dump,
        filters.unknown.dump
    ]

    detector_list = [
        detectors.sdl.detect,
        detectors.lua.detect,
        detectors.tale.detect
    ]

    sys.argv = sys.argv[1:]  # Remove script path

    for dir in sys.argv:
        print(f'Game: {os.path.basename(dir)}')
        data = dump(dir, filter_list, detector_list)

        for key, value in data.items():
            print(f'{key}: {value}')

        print()


if __name__ == '__main__':
    main()