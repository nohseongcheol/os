#!/usr/bin/env python3
"""বাংলা C 식별자만 UCN으로 옮긴다. স্ট্রিং_মান·문자·주석·include 파일명은 보존한다."""
import argparse
from pathlib import Path
import re

টোকেন_মান = re.compile(r'(?P<보존>//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|^[ \t]*#[ \t]*include[ \t]*<[^>]*>)|(?P<সনাক্তকারী_মান>[^\W\d]\w*)', re.S | re.M)

def 변환(উৎস_নথি):
    def প্রতিস্থাপন_করা_মান(일치):
        if 일치.lastgroup == '보존':
            return 일치[0]
        return ''.join(অক্ষর_মান if ord(অক্ষর_মান) < 128 else
                       ('\\u%04x' if ord(অক্ষর_মান) <= 65535 else '\\U%08x') % ord(অক্ষর_মান)
                       for অক্ষর_মান in 일치[0])
    return টোকেন_মান.sub(প্রতিস্থাপন_করা_মান, উৎস_নথি)

def কার্যকর_করুন_আদেশ():
    পার্সার_48ee4b1b = argparse.ArgumentParser()
    পার্সার_48ee4b1b.add_argument('원본', type=Path)
    পার্সার_48ee4b1b.add_argument('নির্গম', type=Path)
    আর্গুমেন্ট_তালিকা = পার্সার_48ee4b1b.parse_args()
    for নথির_নাম in sorted(আর্গুমেন্ট_তালিকা.원본.rglob('*')):
        if নথির_নাম.suffix not in ('.c', '.h'):
            continue
        নির্গম = আর্গুমেন্ট_তালিকা.নির্গম / নথির_নাম.relative_to(আর্গুমেন্ট_তালিকা.원본)
        নির্গম.parent.mkdir(parents=True, exist_ok=True)
        새원문 = 변환(নথির_নাম.read_text())
        if not নির্গম.exists() or নির্গম.read_text() != 새원문:
            নির্গম.write_text(새원문)

if __name__ == '__main__':
    কার্যকর_করুন_আদেশ()
