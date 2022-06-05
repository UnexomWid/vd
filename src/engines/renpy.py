# Detects games made with Ren'Py
import os


def detect(path, exes, dlls):
    # Strategy:
    # - check the 'renpy' folder, it should have a file named '__init__.py' holding the version info
    # - the file could be directly imported; however, this leads to arbitrary code execution
    # - it's safer to manually parse the file

    init_path = os.path.join(path, 'renpy', '__init__.py')

    if not os.path.exists(init_path):
        return

    version_numbers = []

    with open(init_path, 'rt') as init:
        for line in init:
            content = line.strip().lower()

            if not content.startswith('version_tuple'):
                continue

            # Example:
            # version_tuple = (7, 3, 5, vc_version) <--- this can also have 5 or more elements
            #
            # vc_version is the revision number, and is stored in another script
            # From what I've seen, vc_version has something to do with the commits
            # (https://github.com/renpy/renpy/blob/master/distribute.py)
            data = content.split('=')[1].strip()[1:-1].split(',')

            for i in range(len(data) - 1):  # Exclude vc_version
                version_numbers.append(data[i].strip())

    # Read vc_version from another file, since it's not stored in init
    vc_version = os.path.join(path, 'renpy', 'vc_version.py')

    if os.path.exists(vc_version):
        with open(vc_version, 'rt') as vc:
            for line in vc:
                content = line.strip().lower()

                if not content.startswith('vc_version'):
                    continue

                # Example:
                # vc_version = 606
                version_numbers.append(content.split('=')[1].strip())  # Revision

                break

    if len(version_numbers) == 0:
        # No version found in the __init__.py file, and no revision number in vc_version.py
        return {
            'Engine': "Ren'Py (unknown version)"
        }

    if len(version_numbers) == 1:
        # No version found in __init__.py file, but a revision number was found in vc_version.py
        return {
            'Engine': f"Ren'Py (unknown version, revision {version_numbers[0]})"
        }

    return {
        'Engine': f"Ren'Py ({'.'.join(version_numbers)})"
    }
