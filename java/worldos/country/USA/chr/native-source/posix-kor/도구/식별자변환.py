#!/usr/bin/env python3
"""한국어 C 식별자만 UCN으로 옮긴다. ᎠᏍᏘ_ᏧᎬᏩᎶᏗᏯ·문자·주석·include 파일명은 보존한다."""
import argparse
from pathlib import Path
import re

토큰 = re.compile(r'(?P<보존>//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|^[ \t]*#[ \t]*include[ \t]*<[^>]*>)|(?P<ᎠᏓᏙᎵᎩ_ᏧᎬᏩᎶᏗᏯ>[^\W\d]\w*)', re.S | re.M)

def 변환(ᎦᏟᏌᏅᎯ_0201f362):
    def ᎯᏁᏟᏴᏍᏓ_ᏧᎬᏩᎶᏗᏯ(일치):
        if 일치.lastgroup == '보존':
            return 일치[0]
        return ''.join(ᎪᏪᎸ_ᏧᎬᏩᎶᏗᏯ if ord(ᎪᏪᎸ_ᏧᎬᏩᎶᏗᏯ) < 128 else
                       ('\\u%04x' if ord(ᎪᏪᎸ_ᏧᎬᏩᎶᏗᏯ) <= 65535 else '\\U%08x') % ord(ᎪᏪᎸ_ᏧᎬᏩᎶᏗᏯ)
                       for ᎪᏪᎸ_ᏧᎬᏩᎶᏗᏯ in 일치[0])
    return 토큰.sub(ᎯᏁᏟᏴᏍᏓ_ᏧᎬᏩᎶᏗᏯ, ᎦᏟᏌᏅᎯ_0201f362)

def ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ():
    해석기 = argparse.ArgumentParser()
    해석기.add_argument('원본', type=Path)
    해석기.add_argument('출력', type=Path)
    인수 = 해석기.parse_args()
    for ᎠᏍᏆᏂᎪᏙᏗ in sorted(인수.원본.rglob('*')):
        if ᎠᏍᏆᏂᎪᏙᏗ.suffix not in ('.c', '.h'):
            continue
        출력 = 인수.출력 / ᎠᏍᏆᏂᎪᏙᏗ.relative_to(인수.원본)
        출력.parent.mkdir(parents=True, exist_ok=True)
        새원문 = 변환(ᎠᏍᏆᏂᎪᏙᏗ.read_text())
        if not 출력.exists() or 출력.read_text() != 새원문:
            출력.write_text(새원문)

if __name__ == '__main__':
    ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ()
