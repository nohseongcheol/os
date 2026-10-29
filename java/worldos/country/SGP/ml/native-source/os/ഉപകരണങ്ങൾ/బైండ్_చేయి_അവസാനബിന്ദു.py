#!/usr/bin/env python3
"""명시한 ഉപയോക്താവ് ELF만 വായന 전용 JKAP 묶음에 넣는다. 기존 디스크는 사용하지 않는다."""
import argparse
from pathlib import Path
import re
import struct

def బైండ్_చేయి_അവസാനബിന്ദു():
    പാര്_സ്_ചെയ്യുക_മൂല്യം = argparse.ArgumentParser()
    പാര്_സ്_ചെയ്യുക_മൂല്യം.add_argument('-o', required=True)
    പാര്_സ്_ചെയ്യുക_മൂല്യം.add_argument('files', nargs='+', help='പേരു്=ELF경로')
    പാരാമീറ്റര്_ആര്_ഗ്യുമെന്_റ് = പാര്_സ്_ചെയ്യുക_മൂല്യം.parse_args()
    if len(പാരാമീറ്റര്_ആര്_ഗ്യുമെന്_റ്.files) > 32:
        പാര്_സ്_ചെയ്യുക_മൂല്യം.error('പ്രോഗ്രാം_f5044b9b 최대 32개')
    항목들 = []
    이름들 = set()
    for എന്_ട്രി_മൂല്യം in പാരാമീറ്റര്_ആര്_ഗ്യുമെന്_റ്.files:
        പേരു്, വഴി = എന്_ട്രി_മൂല്യം.split('=', 1)
        if not re.fullmatch('[a-z][a-z0-9_-]{0,14}', പേരു്) or പേരു് in 이름들:
            പാര്_സ്_ചെയ്യുക_മൂല്യം.error('നടപ്പാക്കുക_കമാന്_ഡ് 이름이 잘못되었거나 중복됨: ' + പേരു്)
        이름들.add(പേരു്)
        ഡാറ്റാ = Path(വഴി).read_bytes()
        if len(ഡാറ്റാ) > 2 * 1024 * 1024:
            പാര്_സ്_ചെയ്യുക_മൂല്യം.error('നടപ്പാക്കുക_കമാന്_ഡ് 파일이 너무 큼')
        항목들.append((പേരു്.encode(), ഡാറ്റാ))
    അളവ് = bytearray(8 + 24 * len(항목들))
    struct.pack_into('<II', അളവ്, 0, 0x50414b4a, len(항목들))
    for സൂചിക, (പേരു്, ഡാറ്റാ) in enumerate(항목들):
        അളവ്.extend(bytes((-len(അളവ്)) % 16))
        struct.pack_into('<16sII', അളവ്, 8 + സൂചിക * 24, പേരു്, len(അളവ്), len(ഡാറ്റാ))
        അളവ്.extend(ഡാറ്റാ)
    Path(പാരാമീറ്റര്_ആര്_ഗ്യുമെന്_റ്.o).write_bytes(അളവ്)

if __name__ == '__main__':
    బైండ్_చేయి_അവസാനബിന്ദു()
