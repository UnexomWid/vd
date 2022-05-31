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


def dump(path, filters):
    # TODO: try except
    for filter in filters:
        result = filter(path)

        if result is not None:
            return result

    return {}


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

    sys.argv = sys.argv[1:]  # Remove script path

    for dir in sys.argv:
        print(f'Game: {os.path.basename(dir)}')
        data = dump(dir, filter_list)

        for key, value in data.items():
            print(f'{key}: {value}\n')


if __name__ == '__main__':
    main()