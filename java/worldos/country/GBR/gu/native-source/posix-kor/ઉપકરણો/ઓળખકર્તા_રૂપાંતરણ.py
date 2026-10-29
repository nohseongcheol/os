#!/usr/bin/env python3
"""ગુજરાતી C 식별자만 UCN으로 옮긴다. સ્ટ્રિંગ_મૂલ્ય·문자·주석·include 파일명은 보존한다."""
import argparse
from pathlib import Path
import re

ટોકન_મૂલ્ય = re.compile(r'(?P<보존>//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|^[ \t]*#[ \t]*include[ \t]*<[^>]*>)|(?P<ઓળખકર્તા_મૂલ્ય>[^\W\d]\w*)', re.S | re.M)

def 변환(સ્રોત):
    def બદલો_મૂલ્ય(일치):
        if 일치.lastgroup == '보존':
            return 일치[0]
        return ''.join(વર્ણ_મૂલ્ય if ord(વર્ણ_મૂલ્ય) < 128 else
                       ('\\u%04x' if ord(વર્ણ_મૂલ્ય) <= 65535 else '\\U%08x') % ord(વર્ણ_મૂલ્ય)
                       for વર્ણ_મૂલ્ય in 일치[0])
    return ટોકન_મૂલ્ય.sub(બદલો_મૂલ્ય, સ્રોત)

def અમલ_કરો_આદેશ():
    해석기 = argparse.ArgumentParser()
    해석기.add_argument('원본', type=Path)
    해석기.add_argument('આઉટપુટ', type=Path)
    દલીલો = 해석기.parse_args()
    for ફાઈલ in sorted(દલીલો.원본.rglob('*')):
        if ફાઈલ.suffix not in ('.c', '.h'):
            continue
        આઉટપુટ = દલીલો.આઉટપુટ / ફાઈલ.relative_to(દલીલો.원본)
        આઉટપુટ.parent.mkdir(parents=True, exist_ok=True)
        새원문 = 변환(ફાઈલ.read_text())
        if not આઉટપુટ.exists() or આઉટપુટ.read_text() != 새원문:
            આઉટપુટ.write_text(새원문)

if __name__ == '__main__':
    અમલ_કરો_આદેશ()
