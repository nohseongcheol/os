#!/usr/bin/env python3
"""ትግርኛ C 식별자만 UCN으로 옮긴다. ሕብረ_ቁምፊ_ዋጋ·문자·주석·include 파일명은 보존한다."""
import argparse
from pathlib import Path
import re

መፈለጥታ_ዋጋ_eb540501 = re.compile(r'(?P<보존>//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|^[ \t]*#[ \t]*include[ \t]*<[^>]*>)|(?P<ፈላዪ_ዋጋ_5b7b8b77>[^\W\d]\w*)', re.S | re.M)

def 변환(ምንጪ):
    def ተክእ_ዋጋ(일치):
        if 일치.lastgroup == '보존':
            return 일치[0]
        return ''.join(ፊደል_ዋጋ if ord(ፊደል_ዋጋ) < 128 else
                       ('\\u%04x' if ord(ፊደል_ዋጋ) <= 65535 else '\\U%08x') % ord(ፊደል_ዋጋ)
                       for ፊደል_ዋጋ in 일치[0])
    return መፈለጥታ_ዋጋ_eb540501.sub(ተክእ_ዋጋ, ምንጪ)

def ተግብር_ትእዛዝ():
    해석기 = argparse.ArgumentParser()
    해석기.add_argument('원본', type=Path)
    해석기.add_argument('출력', type=Path)
    인수 = 해석기.parse_args()
    for ፋይል in sorted(인수.원본.rglob('*')):
        if ፋይል.suffix not in ('.c', '.h'):
            continue
        출력 = 인수.출력 / ፋይል.relative_to(인수.원본)
        출력.parent.mkdir(parents=True, exist_ok=True)
        새원문 = 변환(ፋይል.read_text())
        if not 출력.exists() or 출력.read_text() != 새원문:
            출력.write_text(새원문)

if __name__ == '__main__':
    ተግብር_ትእዛዝ()
