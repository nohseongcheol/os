#!/usr/bin/env python3
"""English C 식별자만 UCN으로 옮긴다. stringValue·Characters·주석·include 파일명은 보존한다."""
import argparse
from pathlib import Path
import re

tokenValue = re.compile(r'(?P<보존>//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|^[ \t]*#[ \t]*include[ \t]*<[^>]*>)|(?P<identifierValue>[^\W\d]\w*)', re.S | re.M)

def convertValue(source):
    def replaceValue(isEqual):
        if isEqual.lastgroup == '보존':
            return isEqual[0]
        return ''.join(characterValue if ord(characterValue) < 128 else
                       ('\\u%04x' if ord(characterValue) <= 65535 else '\\U%08x') % ord(characterValue)
                       for characterValue in isEqual[0])
    return tokenValue.sub(replaceValue, source)

def executeCommand():
    Parser = argparse.ArgumentParser()
    Parser.add_argument('original', type=Path)
    Parser.add_argument('Output', type=Path)
    arguments = Parser.parse_args()
    for file in sorted(arguments.original.rglob('*')):
        if file.suffix not in ('.c', '.h'):
            continue
        Output = arguments.Output / file.relative_to(arguments.original)
        Output.parent.mkdir(parents=True, exist_ok=True)
        newSource = convertValue(file.read_text())
        if not Output.exists() or Output.read_text() != newSource:
            Output.write_text(newSource)

if __name__ == '__main__':
    executeCommand()
