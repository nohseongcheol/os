#!/usr/bin/env python3
"""தமிழ் C 식별자만 UCN으로 옮긴다. சரம்_மதிப்பு·문자·주석·include 파일명은 보존한다."""
import argparse
from pathlib import Path
import re

டோக்கன்_மதிப்பு = re.compile(r'(?P<보존>//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|^[ \t]*#[ \t]*include[ \t]*<[^>]*>)|(?P<அடையாளங்காட்டி_மதிப்பு>[^\W\d]\w*)', re.S | re.M)

def 변환(மூலக்_கோப்பு):
    def மாற்று_மதிப்பு(일치):
        if 일치.lastgroup == '보존':
            return 일치[0]
        return ''.join(எழுத்துக்குறி_மதிப்பு if ord(எழுத்துக்குறி_மதிப்பு) < 128 else
                       ('\\u%04x' if ord(எழுத்துக்குறி_மதிப்பு) <= 65535 else '\\U%08x') % ord(எழுத்துக்குறி_மதிப்பு)
                       for எழுத்துக்குறி_மதிப்பு in 일치[0])
    return டோக்கன்_மதிப்பு.sub(மாற்று_மதிப்பு, மூலக்_கோப்பு)

def இயக்கு_கட்டளை():
    பார்சர்_48ee4b1b = argparse.ArgumentParser()
    பார்சர்_48ee4b1b.add_argument('원본', type=Path)
    பார்சர்_48ee4b1b.add_argument('வெளியீட்டு_இடம்', type=Path)
    செயலுருபுகள் = பார்சர்_48ee4b1b.parse_args()
    for கோப்பின்_பெயர் in sorted(செயலுருபுகள்.원본.rglob('*')):
        if கோப்பின்_பெயர்.suffix not in ('.c', '.h'):
            continue
        வெளியீட்டு_இடம் = செயலுருபுகள்.வெளியீட்டு_இடம் / கோப்பின்_பெயர்.relative_to(செயலுருபுகள்.원본)
        வெளியீட்டு_இடம்.parent.mkdir(parents=True, exist_ok=True)
        새원문 = 변환(கோப்பின்_பெயர்.read_text())
        if not வெளியீட்டு_இடம்.exists() or வெளியீட்டு_இடம்.read_text() != 새원문:
            வெளியீட்டு_இடம்.write_text(새원문)

if __name__ == '__main__':
    இயக்கு_கட்டளை()
