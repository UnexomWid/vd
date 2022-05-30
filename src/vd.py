import sys
import os

import filters.unity
import filters.renpy
import filters.nscripter
import filters.xna
import filters.unreal
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
        filters.nscripter.dump,
        filters.xna.dump,
        filters.unreal.dump,
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