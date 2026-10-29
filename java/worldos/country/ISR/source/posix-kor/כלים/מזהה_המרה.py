#!/usr/bin/env python3
"""עברית C 식별자만 UCN으로 옮긴다. מחרוזת_ערך·문자·주석·include 파일명은 보존한다."""
import argparse
from pathlib import Path
import re

אסימון_ערך = re.compile(r'(?P<보존>//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|^[ \t]*#[ \t]*include[ \t]*<[^>]*>)|(?P<מזהה_ערך>[^\W\d]\w*)', re.S | re.M)

def המר_ערך(קודמקור):
    def 바꾸기(일치):
        if 일치.lastgroup == '보존':
            return 일치[0]
        return ''.join(תו_ערך if ord(תו_ערך) < 128 else
                       ('\\u%04x' if ord(תו_ערך) <= 65535 else '\\U%08x') % ord(תו_ערך)
                       for תו_ערך in 일치[0])
    return אסימון_ערך.sub(바꾸기, קודמקור)

def לבצע_פקודה():
    מנתח_48ee4b1b = argparse.ArgumentParser()
    מנתח_48ee4b1b.add_argument('원본', type=Path)
    מנתח_48ee4b1b.add_argument('פלטטקסט', type=Path)
    ארגומנטים = מנתח_48ee4b1b.parse_args()
    for קובץ in sorted(ארגומנטים.원본.rglob('*')):
        if קובץ.suffix not in ('.c', '.h'):
            continue
        פלטטקסט = ארגומנטים.פלטטקסט / קובץ.relative_to(ארגומנטים.원본)
        פלטטקסט.parent.mkdir(parents=True, exist_ok=True)
        새원문 = המר_ערך(קובץ.read_text())
        if not פלטטקסט.exists() or פלטטקסט.read_text() != 새원문:
            פלטטקסט.write_text(새원문)

if __name__ == '__main__':
    לבצע_פקודה()
