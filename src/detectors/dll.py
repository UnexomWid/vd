# Detects if a game uses various libs/frameworks
# based on which DLL files are present
import re


ENTRIES = [
    (re.compile(r'^SDL\.dll$'), 'SDL'),
    (re.compile(r'^SDL2\.dll$'), 'SDL2'),
    (re.compile(r'^Antlr3.Runtime\.dll$'), 'ANTLR3 (.Net)'),
    (re.compile(r'^Antlr4.Runtime\.dll$'), 'ANTLR4 (.Net)'),
    (re.compile(r'^libcurl\.dll$'), 'curl'),
    (re.compile(r'^Lidgren(.*)\.dll$'), 'Lidgren'),
    (re.compile(r'^lua(.*)\.dll$'), 'Lua'),
    (re.compile(r'^Tale\.dll$'), 'Tale'),
    (re.compile(r'^(.*)Naninovel(.*)\.dll$'), 'Naninovel')
]


def detect(path, exes, dlls):
    results = []

    for entry in ENTRIES:
        if any(filter(entry[0].match, dlls)):
            results.append(entry[1])

    return results
