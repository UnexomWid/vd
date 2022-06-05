# Detects games made with Ethornell (Buriko General Interpreter)
import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], '..'))
from utils.pe import get_version_info


def detect(path, exes, dlls):
    # Strategy:
    # - check the exe version info for interesting strings:
    #   - InternalName: Ethornell
    #   - FileDescription: Ethornell - BURIKO General Interpreter

    for exe in exes:
        info = get_version_info(os.path.join(path, exe))

        if not info:
            continue

        if 'InternalName' in info and 'Ethornell' in info['InternalName']:
            return {
                'Engine': 'BGI/Ethornell'
            }

        if 'FileDescription' in info and 'Ethornell' in info['FileDescription']:
            return {
                'Engine': 'BGI/Ethornell'
            }
