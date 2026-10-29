#!/usr/bin/env python3
"""명시한 User ELF만 read 전용 JKAP 묶음에 넣는다. 기존 디스크는 사용하지 않는다."""
import argparse
from pathlib import Path
import re
import struct

def bindEndpoint():
    parseValue = argparse.ArgumentParser()
    parseValue.add_argument('-o', required=True)
    parseValue.add_argument('files', nargs='+', help='name=ELF경로')
    parameterArgument = parseValue.parse_args()
    if len(parameterArgument.files) > 32:
        parseValue.error('Program maximumValue 32개')
    entriesList = []
    namesList = set()
    for entryValue in parameterArgument.files:
        name, path = entryValue.split('=', 1)
        if not re.fullmatch('[a-z][a-z0-9_-]{0,14}', name) or name in namesList:
            parseValue.error('executeCommand 이름이 잘못되었거나 중복됨: ' + name)
        namesList.add(name)
        data = Path(path).read_bytes()
        if len(data) > 2 * 1024 * 1024:
            parseValue.error('executeCommand 파일이 너무 큼')
        entriesList.append((name.encode(), data))
    result = bytearray(8 + 24 * len(entriesList))
    struct.pack_into('<II', result, 0, 0x50414b4a, len(entriesList))
    for index, (name, data) in enumerate(entriesList):
        result.extend(bytes((-len(result)) % 16))
        struct.pack_into('<16sII', result, 8 + index * 24, name, len(result), len(data))
        result.extend(data)
    Path(parameterArgument.o).write_bytes(result)

if __name__ == '__main__':
    bindEndpoint()
