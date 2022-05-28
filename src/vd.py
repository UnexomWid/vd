import sys
import os

import filters.unity
import filters.unknown


def dump(path, filters):
    # TODO: try except
    for filter in filters:
        result = filter(path)

        if result is not None:
            return result

    return {}


def main():
    if len(sys.argv) > 1:
        dir = sys.argv[1]
    else:
        dir = os.getcwd()

    filter_list = [
        filters.unity.dump,
        filters.unknown.dump
    ]

    data = dump(dir, filter_list)

    for key, value in data.items():
        print(f'{key}: {value}\n')


if __name__ == '__main__':
    main()