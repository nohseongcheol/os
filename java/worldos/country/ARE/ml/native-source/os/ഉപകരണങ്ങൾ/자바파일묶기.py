#!/usr/bin/env python3
"""명시한 Java ഉറവിടം_ശാഖി/ക്ലാസ്_മൂല്യം 파일을 부팅 시 RAM 파일체계로 가져온다."""
import argparse
from pathlib import Path
import re
import struct


def బైండ్_చేయి_അവസാനബിന്ദു(항목들):
    파일들 = []
    이름들 = {'Hello.java'}
    명시 = set()
    for എന്_ട്രി_മൂല്യം in 항목들:
        if '=' not in എന്_ട്രി_മൂല്യം:
            raise ValueError('expected NAME=PATH: ' + എന്_ട്രി_മൂല്യം)
        പേരു്, വഴി = എന്_ട്രി_മൂല്യം.split('=', 1)
        if not re.fullmatch(r'[A-Za-z0-9_-][A-Za-z0-9_.-]{0,62}', പേരു്) or പേരു് in 명시:
            raise ValueError('invalid or duplicate file name: ' + പേരു്)
        명시.add(പേരു്)
        이름들.add(പേരു്)
        ഡാറ്റാ = Path(വഴി).read_bytes()
        if len(ഡാറ്റാ) > 16384:
            raise ValueError('file exceeds 16384 bytes: ' + പേരു്)
        파일들.append((പേരു്.encode('ascii'), ഡാറ്റാ))
    if len(이름들) > 8:
        raise ValueError('RAM file limit: 8 files including the default Hello.java')
    അളവ് = bytearray(struct.pack('<4sI', b'JKJF', len(파일들)))
    അളവ്.extend(bytes(72 * len(파일들)))
    for 수, (പേരു്, ഡാറ്റാ) in enumerate(파일들):
        struct.pack_into('<64sII', അളവ്, 8 + 수 * 72, പേരു്, len(അളവ്), len(ഡാറ്റാ))
        അളവ്.extend(ഡാറ്റാ)
    return bytes(അളവ്)


if __name__ == '__main__':
    പാര്_സ്_ചെയ്യുക_മൂല്യം = argparse.ArgumentParser(description=__doc__)
    പാര്_സ്_ചെയ്യുക_മൂല്യം.add_argument('-o', required=True)
    പാര്_സ്_ചെയ്യുക_മൂല്യം.add_argument('files', nargs='*', help='NAME=PATH')
    인수 = പാര്_സ്_ചെയ്യുക_മൂല്യം.parse_args()
    try:
        ഡാറ്റാ = బైండ్_చేయి_അവസാനബിന്ദു(인수.files)
        ഉദ്ദിഷ്ടസ്ഥാനം_മൂല്യം = Path(인수.o)
        if not ഉദ്ദിഷ്ടസ്ഥാനം_മൂല്യം.exists() or ഉദ്ദിഷ്ടസ്ഥാനം_മൂല്യം.read_bytes() != ഡാറ്റാ:
            임시 = ഉദ്ദിഷ്ടസ്ഥാനം_മൂല്യം.with_name(ഉദ്ദിഷ്ടസ്ഥാനം_മൂല്യം.name + '.tmp')
            임시.write_bytes(ഡാറ്റാ)
            임시.replace(ഉദ്ദിഷ്ടസ്ഥാനം_മൂല്യം)
    except (ValueError, OSError) as പിശക്:
        പാര്_സ്_ചെയ്യുക_മൂല്യം.error(str(പിശക്))
