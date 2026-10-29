#!/usr/bin/env python3
"""명시한 Java sourceTree/classValue 파일을 machine_boot 시 RAM 파일체계로 가져온다."""
import argparse
from pathlib import Path
import re
import struct


def bindEndpoint(entriesList):
    fileEntries = []
    namesList = {'Hello.java'}
    explicitNames = set()
    for entryValue in entriesList:
        if '=' not in entryValue:
            raise ValueError('expected NAME=PATH: ' + entryValue)
        name, path = entryValue.split('=', 1)
        if not re.fullmatch(r'[A-Za-z0-9_-][A-Za-z0-9_.-]{0,62}', name) or name in explicitNames:
            raise ValueError('invalid or duplicate file name: ' + name)
        explicitNames.add(name)
        namesList.add(name)
        data = Path(path).read_bytes()
        if len(data) > 16384:
            raise ValueError('file exceeds 16384 bytes: ' + name)
        fileEntries.append((name.encode('ascii'), data))
    if len(namesList) > 8:
        raise ValueError('RAM file limit: 8 files including the default Hello.java')
    result = bytearray(struct.pack('<4sI', b'JKJF', len(fileEntries)))
    result.extend(bytes(72 * len(fileEntries)))
    for number, (name, data) in enumerate(fileEntries):
        struct.pack_into('<64sII', result, 8 + number * 72, name, len(result), len(data))
        result.extend(data)
    return bytes(result)


if __name__ == '__main__':
    parseValue = argparse.ArgumentParser(description=__doc__)
    parseValue.add_argument('-o', required=True)
    parseValue.add_argument('files', nargs='*', help='NAME=PATH')
    arguments = parseValue.parse_args()
    try:
        data = bindEndpoint(arguments.files)
        destinationValue = Path(arguments.o)
        if not destinationValue.exists() or destinationValue.read_bytes() != data:
            temporaryValue = destinationValue.with_name(destinationValue.name + '.tmp')
            temporaryValue.write_bytes(data)
            temporaryValue.replace(destinationValue)
    except (ValueError, OSError) as error:
        parseValue.error(str(error))
