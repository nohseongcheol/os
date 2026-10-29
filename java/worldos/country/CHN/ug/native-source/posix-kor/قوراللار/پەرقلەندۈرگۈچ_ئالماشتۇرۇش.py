#!/usr/bin/env python3
"""한국어 C 식별자만 UCN으로 옮긴다. ھەرپ_تىزمىسى_قىممىتى·문자·주석·include 파일명은 보존한다."""
import argparse
from pathlib import Path
import re

ئالدىن_تۆلەش_كارتىسى_كودى_قىممىتى = re.compile(r'(?P<보존>//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|^[ \t]*#[ \t]*include[ \t]*<[^>]*>)|(?P<پەرقلەندۈرگۈچ_قىممىتى>[^\W\d]\w*)', re.S | re.M)

def 변환(مەنبە):
    def ئالماشتۇرماق_قىممىتى(일치):
        if 일치.lastgroup == '보존':
            return 일치[0]
        return ''.join(ھەرپ_بەلگە_قىممىتى if ord(ھەرپ_بەلگە_قىممىتى) < 128 else
                       ('\\u%04x' if ord(ھەرپ_بەلگە_قىممىتى) <= 65535 else '\\U%08x') % ord(ھەرپ_بەلگە_قىممىتى)
                       for ھەرپ_بەلگە_قىممىتى in 일치[0])
    return ئالدىن_تۆلەش_كارتىسى_كودى_قىممىتى.sub(ئالماشتۇرماق_قىممىتى, مەنبە)

def ئىجرا_قىلىش_بۇيرۇق():
    해석기 = argparse.ArgumentParser()
    해석기.add_argument('원본', type=Path)
    해석기.add_argument('چىقار', type=Path)
    ئۆزگەرگۈچىلەر = 해석기.parse_args()
    for ھۆججەت in sorted(ئۆزگەرگۈچىلەر.원본.rglob('*')):
        if ھۆججەت.suffix not in ('.c', '.h'):
            continue
        چىقار = ئۆزگەرگۈچىلەر.چىقار / ھۆججەت.relative_to(ئۆزگەرگۈچىلەر.원본)
        چىقار.parent.mkdir(parents=True, exist_ok=True)
        새원문 = 변환(ھۆججەت.read_text())
        if not چىقار.exists() or چىقار.read_text() != 새원문:
            چىقار.write_text(새원문)

if __name__ == '__main__':
    ئىجرا_قىلىش_بۇيرۇق()
