#!/usr/bin/env python3
"""Indonesia C 식별자만 UCN으로 옮긴다. string_VALUE·문자·주석·include 파일명은 보존한다."""
import argparse
from pathlib import Path
import re

token_VALUE = re.compile(r'(?P<보존>//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|^[ \t]*#[ \t]*include[ \t]*<[^>]*>)|(?P<pengidentifikasi_VALUE>[^\W\d]\w*)', re.S | re.M)

def CONVERT_VALUE(kodeSumber):
    def ganti_VALUE(일치):
        if 일치.lastgroup == '보존':
            return 일치[0]
        return ''.join(karakter_VALUE if ord(karakter_VALUE) < 128 else
                       ('\\u%04x' if ord(karakter_VALUE) <= 65535 else '\\U%08x') % ord(karakter_VALUE)
                       for karakter_VALUE in 일치[0])
    return token_VALUE.sub(ganti_VALUE, kodeSumber)

def Jalankan_perintah():
    parser_48ee4b1b = argparse.ArgumentParser()
    parser_48ee4b1b.add_argument('원본', type=Path)
    parser_48ee4b1b.add_argument('keluaranTeks', type=Path)
    argumen = parser_48ee4b1b.parse_args()
    for berkas in sorted(argumen.원본.rglob('*')):
        if berkas.suffix not in ('.c', '.h'):
            continue
        keluaranTeks = argumen.keluaranTeks / berkas.relative_to(argumen.원본)
        keluaranTeks.parent.mkdir(parents=True, exist_ok=True)
        새원문 = CONVERT_VALUE(berkas.read_text())
        if not keluaranTeks.exists() or keluaranTeks.read_text() != 새원문:
            keluaranTeks.write_text(새원문)

if __name__ == '__main__':
    Jalankan_perintah()
