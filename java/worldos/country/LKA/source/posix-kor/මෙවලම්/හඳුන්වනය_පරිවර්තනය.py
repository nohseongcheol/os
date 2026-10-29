#!/usr/bin/env python3
"""한국어 C 식별자만 UCN으로 옮긴다. අනුලකුණු_වැල_අගය·문자·주석·include 파일명은 보존한다."""
import argparse
from pathlib import Path
import re

සලාකය_අගය = re.compile(r'(?P<보존>//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|^[ \t]*#[ \t]*include[ \t]*<[^>]*>)|(?P<හඳුන්වනය_අගය>[^\W\d]\w*)', re.S | re.M)

def 변환(මූලය):
    def ප්_රතිස්ථාපනය_කරන්න_අගය(일치):
        if 일치.lastgroup == '보존':
            return 일치[0]
        return ''.join(අනුලකුණ_අගය if ord(අනුලකුණ_අගය) < 128 else
                       ('\\u%04x' if ord(අනුලකුණ_අගය) <= 65535 else '\\U%08x') % ord(අනුලකුණ_අගය)
                       for අනුලකුණ_අගය in 일치[0])
    return සලාකය_අගය.sub(ප්_රතිස්ථාපනය_කරන්න_අගය, මූලය)

def ක්_රියාත්මක_කරන්න_විධානය():
    해석기 = argparse.ArgumentParser()
    해석기.add_argument('원본', type=Path)
    해석기.add_argument('출력', type=Path)
    විස්තාරක = 해석기.parse_args()
    for ගොනු in sorted(විස්තාරක.원본.rglob('*')):
        if ගොනු.suffix not in ('.c', '.h'):
            continue
        출력 = විස්තාරක.출력 / ගොනු.relative_to(විස්තාරක.원본)
        출력.parent.mkdir(parents=True, exist_ok=True)
        새원문 = 변환(ගොනු.read_text())
        if not 출력.exists() or 출력.read_text() != 새원문:
            출력.write_text(새원문)

if __name__ == '__main__':
    ක්_රියාත්මක_කරන්න_විධානය()
