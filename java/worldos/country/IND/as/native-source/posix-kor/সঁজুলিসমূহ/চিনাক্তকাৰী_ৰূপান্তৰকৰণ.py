#!/usr/bin/env python3
"""한국어 C 식별자만 UCN으로 옮긴다. ষ্ট্ৰিং_মান·문자·주석·include 파일명은 보존한다."""
import argparse
from pathlib import Path
import re

ট_কেন_মান = re.compile(r'(?P<보존>//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|^[ \t]*#[ \t]*include[ \t]*<[^>]*>)|(?P<চিনাক্তকাৰী_মান>[^\W\d]\w*)', re.S | re.M)

def 변환(উৎস):
    def পুনঃস্থাপন_কৰক_মান(일치):
        if 일치.lastgroup == '보존':
            return 일치[0]
        return ''.join(বৰ্ণ_মান if ord(বৰ্ণ_মান) < 128 else
                       ('\\u%04x' if ord(বৰ্ণ_মান) <= 65535 else '\\U%08x') % ord(বৰ্ণ_মান)
                       for বৰ্ণ_মান in 일치[0])
    return ট_কেন_মান.sub(পুনঃস্থাপন_কৰক_মান, উৎস)

def নিষ্পাদন_আদেশ():
    해석기 = argparse.ArgumentParser()
    해석기.add_argument('원본', type=Path)
    해석기.add_argument('নিৰ্গম', type=Path)
    인수 = 해석기.parse_args()
    for নথিপত্ৰ in sorted(인수.원본.rglob('*')):
        if নথিপত্ৰ.suffix not in ('.c', '.h'):
            continue
        নিৰ্গম = 인수.নিৰ্গম / নথিপত্ৰ.relative_to(인수.원본)
        নিৰ্গম.parent.mkdir(parents=True, exist_ok=True)
        새원문 = 변환(নথিপত্ৰ.read_text())
        if not নিৰ্গম.exists() or নিৰ্গম.read_text() != 새원문:
            নিৰ্গম.write_text(새원문)

if __name__ == '__main__':
    নিষ্পাদন_আদেশ()
