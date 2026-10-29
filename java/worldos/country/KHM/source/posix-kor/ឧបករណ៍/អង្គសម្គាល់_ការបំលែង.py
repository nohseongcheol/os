#!/usr/bin/env python3
"""한국어 C 식별자만 UCN으로 옮긴다. សំនុំអក្សរ_តំលៃ·문자·주석·include 파일명은 보존한다."""
import argparse
from pathlib import Path
import re

កាក់_តំលៃ = re.compile(r'(?P<보존>//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|^[ \t]*#[ \t]*include[ \t]*<[^>]*>)|(?P<អង្គសម្គាល់_តំលៃ>[^\W\d]\w*)', re.S | re.M)

def 변환(ប្រភព):
    def ជំនួស_តំលៃ(일치):
        if 일치.lastgroup == '보존':
            return 일치[0]
        return ''.join(តួអក្សរ_តំលៃ if ord(តួអក្សរ_តំលៃ) < 128 else
                       ('\\u%04x' if ord(តួអក្សរ_តំលៃ) <= 65535 else '\\U%08x') % ord(តួអក្សរ_តំលៃ)
                       for តួអក្សរ_តំលៃ in 일치[0])
    return កាក់_តំលៃ.sub(ជំនួស_តំលៃ, ប្រភព)

def អនុវត្ត_ពាក្យបញ្ជា():
    មុខងារ_ញែក_48ee4b1b = argparse.ArgumentParser()
    មុខងារ_ញែក_48ee4b1b.add_argument('원본', type=Path)
    មុខងារ_ញែក_48ee4b1b.add_argument('លទ្ធផល', type=Path)
    អាគុយម៉ង់ = មុខងារ_ញែក_48ee4b1b.parse_args()
    for ឯកសារ in sorted(អាគុយម៉ង់.원본.rglob('*')):
        if ឯកសារ.suffix not in ('.c', '.h'):
            continue
        លទ្ធផល = អាគុយម៉ង់.លទ្ធផល / ឯកសារ.relative_to(អាគុយម៉ង់.원본)
        លទ្ធផល.parent.mkdir(parents=True, exist_ok=True)
        새원문 = 변환(ឯកសារ.read_text())
        if not លទ្ធផល.exists() or លទ្ធផល.read_text() != 새원문:
            លទ្ធផល.write_text(새원문)

if __name__ == '__main__':
    អនុវត្ត_ពាក្យបញ្ជា()
