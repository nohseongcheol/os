#!/usr/bin/env python3
"""አማርኛ C 식별자만 UCN으로 옮긴다. ኅብረቁምፊ_እሴት·문자·주석·include 파일명은 보존한다."""
import argparse
from pathlib import Path
import re

ቦኖ_እሴት = re.compile(r'(?P<보존>//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|^[ \t]*#[ \t]*include[ \t]*<[^>]*>)|(?P<መለያ_እሴት_5b7b8b77>[^\W\d]\w*)', re.S | re.M)

def 변환(ምንጭ):
    def ተካ_እሴት(일치):
        if 일치.lastgroup == '보존':
            return 일치[0]
        return ''.join(ቁምፊ_እሴት if ord(ቁምፊ_እሴት) < 128 else
                       ('\\u%04x' if ord(ቁምፊ_እሴት) <= 65535 else '\\U%08x') % ord(ቁምፊ_እሴት)
                       for ቁምፊ_እሴት in 일치[0])
    return ቦኖ_እሴት.sub(ተካ_እሴት, ምንጭ)

def ፈጽም_ትእዛዝ():
    አግልሎ_ማስቀመጥ_48ee4b1b = argparse.ArgumentParser()
    አግልሎ_ማስቀመጥ_48ee4b1b.add_argument('원본', type=Path)
    አግልሎ_ማስቀመጥ_48ee4b1b.add_argument('ውጤት', type=Path)
    인수 = አግልሎ_ማስቀመጥ_48ee4b1b.parse_args()
    for ፋይል in sorted(인수.원본.rglob('*')):
        if ፋይል.suffix not in ('.c', '.h'):
            continue
        ውጤት = 인수.ውጤት / ፋይል.relative_to(인수.원본)
        ውጤት.parent.mkdir(parents=True, exist_ok=True)
        새원문 = 변환(ፋይል.read_text())
        if not ውጤት.exists() or ውጤት.read_text() != 새원문:
            ውጤት.write_text(새원문)

if __name__ == '__main__':
    ፈጽም_ትእዛዝ()
