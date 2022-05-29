# Detects games made with Unity
import os
import struct


def dump(path):
    #  Strategy:
    # - check all dirs ending with _data, one of them should have a file named resources.assets,
    #   or one named sharedassets0.assets
    # - open that file and try to get the unity version from it
    # - if everything is successful, the game was most likely made in unity
    data_dirs = [dir for dir in os.listdir(path) if dir.lower().endswith('_data')]

    for data in data_dirs:
        assets = os.path.join(path, data, 'resources.assets')

        if not os.path.exists(assets):
            assets = os.path.join(path, data, 'sharedassets0.assets')

        if not os.path.exists(assets):  # Neither file exists
            return

        with open(assets, 'rb') as res:
            # .assets file
            # Inspired by:
            # https://github.com/SeriousCache/UABE

            # uint of 4 bytes (big endian) for the format, offset 0x08 (skip the first 8 bytes)
            res.seek(8, os.SEEK_CUR)
            fmt = struct.unpack('>I', res.read(4))[0]

            if fmt >= 0x16:
                # 4 unknown bytes, 8 metadata size, 8 file size, 8 offset of first file, 1 endianness, 3 unknown, 4 padding
                res.seek(4 + 8 + 8 + 8 + 1 + 3 + 4, os.SEEK_CUR)
            else:
                # Go back and read the sizes
                res.seek(0, os.SEEK_SET)

                # 2 uints of bytes each (big-endian)
                meta_size, file_size = struct.unpack('>II', res.read(8))

                # 4 bytes first file offset, 4 bytes for the format that we read earlier
                res.seek(4 + 4, os.SEEK_CUR)

                if fmt < 9 and file_size < meta_size:
                    # 1 byte endianness
                    res.seek(file_size - meta_size + 1, os.SEEK_SET)
                else:
                    # 1 byte endianness, 3 bytes unknown
                    res.seek(4, os.SEEK_CUR)

            # The version is at the current position, and is null-terminated
            # 32 characters should be enough
            version_str = res.read(32)
            version = ''.join(chr(c) for c in version_str[:version_str.index(b'\0')])

            return {
                'Engine': f'Unity ({version})'
            }
