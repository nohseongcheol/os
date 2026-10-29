#!/usr/bin/env python3
"""Eesti C 식별자만 UCN으로 옮긴다. string_VALUE·문자·주석·include 파일명은 보존한다."""
import argparse
from pathlib import Path
import re

luba_VALUE_eb540501 = re.compile(r'(?P<보존>//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|^[ \t]*#[ \t]*include[ \t]*<[^>]*>)|(?P<identifikaator_VALUE>[^\W\d]\w*)', re.S | re.M)

def CONVERT_VALUE(ALLIKAS):
    def REPLACE_VALUE(일치):
        if 일치.lastgroup == '보존':
            return 일치[0]
        return ''.join(märk_VALUE if ord(märk_VALUE) < 128 else
                       ('\\u%04x' if ord(märk_VALUE) <= 65535 else '\\U%08x') % ord(märk_VALUE)
                       for märk_VALUE in 일치[0])
    return luba_VALUE_eb540501.sub(REPLACE_VALUE, ALLIKAS)

def Täida_käsk():
    parser_48ee4b1b = argparse.ArgumentParser()
    parser_48ee4b1b.add_argument('원본', type=Path)
    parser_48ee4b1b.add_argument('Väljund', type=Path)
    Argumendid = parser_48ee4b1b.parse_args()
    for Fail in sorted(Argumendid.원본.rglob('*')):
        if Fail.suffix not in ('.c', '.h'):
            continue
        Väljund = Argumendid.Väljund / Fail.relative_to(Argumendid.원본)
        Väljund.parent.mkdir(parents=True, exist_ok=True)
        새원문 = CONVERT_VALUE(Fail.read_text())
        if not Väljund.exists() or Väljund.read_text() != 새원문:
            Väljund.write_text(새원문)

if __name__ == '__main__':
    Täida_käsk()
