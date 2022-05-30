# Portable Executable (PE) file helper
import os
import struct

# https://docs.microsoft.com/en-us/windows/win32/menurc/resource-types
RT_VERSION = 16

# https://docs.microsoft.com/en-us/windows/win32/api/verrsrc/ns-verrsrc-vs_fixedfileinfo
VS_FF = [
    ('DEBUG', 0x00000001),
    ('INFOINFERRED', 0x00000010),
    ('PATCHED', 0x00000004),
    ('PRERELEASE', 0x00000002),
    ('PRIVATEBUILD', 0x00000008),
    ('SPECIALBUILD', 0x00000020)
]

VOS = [
    ('DOS', 0x00010000),
    ('NT', 0x00040000),
    ('WINDOWS16', 0x00000001),
    ('WINDOWS32', 0x00000004),
    ('OS216', 0x00020000),
    ('OS232', 0x00030000),
    ('PM16', 0x00000002),
    ('PM32', 0x00000003)
]

VFT = [
    ('APP', 0x00000001),
    ('DLL', 0x00000002),
    ('DRV', 0x00000003),
    ('FONT', 0x00000004),
    ('STATIC_LIB', 0x00000007),
    ('VXD', 0x00000005)
]

VFT2_DRV = [
    ('COMM', 0x0000000A),
    ('DISPLAY', 0x00000004),
    ('INSTALLABLE', 0x00000008),
    ('KEYBOARD', 0x00000002),
    ('LANGUAGE', 0x00000003),
    ('MOUSE', 0x00000005),
    ('NETWORK', 0x00000006),
    ('PRINTER', 0x00000001),
    ('SOUND', 0x00000009),
    ('SYSTEM', 0x00000007),
    ('VERSIONED_PRINTER', 0x0000000C)
]

VFT2_FONT = [
    ('RASTER', 0x00000001),
    ('TRUETYPE', 0x00000003),
    ('VECTOR', 0x00000002)
]


# Reads one UTF-16 string from a file
def _read_utf16_str(pe):
    str = b''
    char = pe.read(2)

    while char != b'\0\0':
        str += char
        char = pe.read(2)

    return str.decode('utf-16')


# Seeks to the nearest offset that satisfies the specified alignment
def _padding(pe, size):
    if pe.tell() % size != 0:
        pe.seek(size - pe.tell() % size, os.SEEK_CUR)


def _dict_append_list(dict, key, value):
    if key not in dict:
        dict[key] = value.strip()
    else:
        dict[key] += f', {value.strip()}'


# https://docs.microsoft.com/en-us/windows/win32/menurc/vs-versioninfo
# The .rsrc section contains multiple nodes
# The leaf node that is a child of the VERSION node has raw data that is parsed here
def parse_version_section(pe):
    result = {}

    start_offset = pe.tell()

    _padding(pe, 4)

    start_struct = pe.tell()

    length, value_length, type = struct.unpack('<HHH', pe.read(6))

    name = _read_utf16_str(pe)

    _padding(pe, 4)

    if name == 'StringFileInfo':
        # https://docs.microsoft.com/en-us/windows/win32/menurc/stringfileinfo
        offset = pe.tell() - start_struct

        # https://docs.microsoft.com/en-us/windows/win32/menurc/stringtable
        while offset < length:
            _padding(pe, 4)

            str_table_start_struct = pe.tell()

            str_table_length, str_table_value_length, str_table_type = struct.unpack('<HHH', pe.read(6))
            str_table_name = _read_utf16_str(pe)
            _padding(pe, 4)

            str_table_offset = pe.tell() - str_table_start_struct

            # https://docs.microsoft.com/en-us/windows/win32/menurc/string-str
            while str_table_offset < str_table_length:
                _padding(pe, 4)

                # str_length, str_value_length, str_type
                pe.seek(6, os.SEEK_CUR)

                str_name = _read_utf16_str(pe)
                _padding(pe, 4)
                str_value = _read_utf16_str(pe)

                if len(str_name.strip()) > 0:
                    result[str_name] = str_value

                str_table_offset = pe.tell() - str_table_start_struct

            offset = pe.tell() - start_struct
    elif name == 'VarFileInfo':
        # https://docs.microsoft.com/en-us/windows/win32/menurc/varfileinfo
        offset = pe.tell() - start_struct

        # https://docs.microsoft.com/en-us/windows/win32/menurc/var-str
        while offset < length:
            #var_length, var_value_length, var_type
            pe.seek(6, os.SEEK_CUR)

            var_name = _read_utf16_str(pe)
            _padding(pe, 4)
            var_value = _read_utf16_str(pe)

            # We don't need VarFileInfo since it contains info about languages
            #
            # if len(var_name.strip()) > 0:
            #     result[var_name] = var_value

            offset = pe.tell() - start_struct
    elif name == 'VS_VERSION_INFO':
        # https://docs.microsoft.com/en-us/windows/win32/api/verrsrc/ns-verrsrc-vs_fixedfileinfo
        pe.seek(4 + 4, os.SEEK_CUR)

        # Mixed endianness: minor_major build_patch
        file_version_minor, file_version_major, file_version_private, file_version_build = struct.unpack('<HHHH', pe.read(8))
        product_version_minor, product_version_major, product_version_private, product_version_build = struct.unpack('<HHHH', pe.read(8))

        file_flags_mask, file_flags = struct.unpack('<II', pe.read(8))
        file_os = struct.unpack('<I', pe.read(4))[0]
        file_type, file_subtype = struct.unpack('<II', pe.read(8))
        # file_date_ms, file_date_ls
        pe.seek(8, os.SEEK_CUR)  # The timestamp seems to always be 0, so skip over it

        result["FileVersionRaw"] = f'{file_version_major}.{file_version_minor}.{file_version_build}.{file_version_private}'
        result["ProductVersionRaw"] = f'{product_version_major}.{product_version_minor}.{product_version_build}.{product_version_private}'

        for flag in VS_FF:
            if file_flags & flag[1] & file_flags_mask:
                _dict_append_list(result, 'FileFlags', flag[0])

        for vos in VOS:
            if file_os & vos[1]:
                _dict_append_list(result, 'FileOS', vos[0])

        if 'FileOS' not in result:
            result['FileOS'] = 'UNKNOWN'

        for type in VFT:
            if file_type & type[1]:
                _dict_append_list(result, 'FileType', type[0])

        if 'FileType' not in result:
            result['FileType'] = 'UNKNOWN'

        if file_type & VFT[2][1]:  # DRV
            for subtype in VFT2_DRV:
                if file_subtype & subtype[1]:
                    _dict_append_list(result, 'FileSubtype', subtype[0])

            if 'FileSubtype' not in result:
                result['FileSubtype'] = 'UNKNOWN'
        elif file_type & VFT[3][1]:  # FONT
            for font in VFT2_FONT:
                if file_subtype & font[1]:
                    _dict_append_list(result, 'FileSubtype', font[0])

            if 'FileSubtype' not in result:
                result['FileSubtype'] = 'UNKNOWN'
    else:
        value = _read_utf16_str(pe)
        if len(name.strip()) > 0:
            result[name] = value

    offset = pe.tell() - start_offset

    while offset < length:
        result.update(parse_version_section(pe))
        offset = pe.tell() - start_offset

    _padding(pe, 4)

    return result


# Takes a path to a PE file and returns the version info from the .rsrc section
def get_version_info(path):
    if not os.path.exists(path):
        return

    with open(path, 'rb') as pe:
        try:
            # All integers are little endian
            magic = pe.read(2)

            if magic != b'MZ':
                return  # Invalid magic

            pe.seek(0x3C, os.SEEK_SET)
            signature_offset = struct.unpack('<I', pe.read(4))[0]
            pe.seek(signature_offset, os.SEEK_SET)

            pe_signature = pe.read(4)

            if pe_signature != b'PE\0\0':
                return  # Invalid PE signature

            pe.seek(2, os.SEEK_CUR)

            number_of_sections = struct.unpack('<H', pe.read(2))[0]

            pe.seek(4 + 4 + 4 + 2 + 2, os.SEEK_CUR)

            optional_header_offset = pe.tell()
            optional_header_magic = struct.unpack('<H', pe.read(2))[0]

            if optional_header_magic == 0x10B:
                # PE32
                pe.seek(optional_header_offset + 224, os.SEEK_SET)
            elif optional_header_magic == 0x20B:
                # PE32+
                pe.seek(optional_header_offset + 240, os.SEEK_SET)
            else:
                return  # Invalid optional header magic

            has_rsrc = False

            for i in range(number_of_sections):
                name = pe.read(8)

                if name == b'.rsrc\0\0\0':
                    has_rsrc = True
                    break

                pe.read(32)
                continue

            if not has_rsrc:
                return

            # .rsrc
            pe.seek(4, os.SEEK_CUR)

            virtual_address, size_of_raw_data, pointer_to_raw_data = struct.unpack('<III', pe.read(12))

            pe.seek(pointer_to_raw_data, os.SEEK_SET)

            # The resource section
            pe.seek(4 + 4 + 2 + 2, os.SEEK_CUR)

            name_entries, id_entries = struct.unpack('<HH', pe.read(4))

            pe.seek(8 * name_entries, os.SEEK_CUR)

            # Walk through the children. Since we only need the VERSION resources,
            # we'll go straight for them and not use recursion.
            for i in range(id_entries):
                id, data = struct.unpack('<II', pe.read(8))

                if not data & (1 << 31):
                    return  # VERSION resource doesn't have a subdirectory

                data = data & ~(1 << 31)

                if id == RT_VERSION:
                    # Subdir start
                    pe.seek(pointer_to_raw_data + data, os.SEEK_SET)
                    pe.seek(4 + 4 + 2 + 2, os.SEEK_CUR)

                    name_entries, id_entries = struct.unpack('<HH', pe.read(4))
                    pe.seek(8 * name_entries, os.SEEK_CUR)

                    # First child of RT_VERSION
                    id, data = struct.unpack('<II', pe.read(8))

                    if not data & (1 << 31):
                        return  # No subdirectory

                    data = data & ~(1 << 31)

                    pe.seek(pointer_to_raw_data + data, os.SEEK_SET)
                    pe.seek(4 + 4 + 2 + 2, os.SEEK_CUR)

                    name_entries, id_entries = struct.unpack('<HH', pe.read(4))
                    pe.seek(8 * name_entries, os.SEEK_CUR)

                    id, data = struct.unpack('<II', pe.read(8))

                    if data & (1 << 31):
                        return  # No raw data

                    # This is the version location
                    pe.seek(pointer_to_raw_data + data, os.SEEK_SET)
                    data = struct.unpack('<I', pe.read(4))[0]
                    pe.seek(pointer_to_raw_data + (data - virtual_address), os.SEEK_SET)

                    # All that's left is to parse the version info itself
                    return parse_version_section(pe)
        except:
            return
