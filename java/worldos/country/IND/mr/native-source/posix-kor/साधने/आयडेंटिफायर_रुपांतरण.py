#!/usr/bin/env python3
"""मराठी C 식별자만 UCN으로 옮긴다. स्ट्रींग_मूल्य·वर्ण·주석·include 파일명은 보존한다."""
import argparse
from pathlib import Path
import re

टोकन_मूल्य = re.compile(r'(?P<보존>//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|^[ \t]*#[ \t]*include[ \t]*<[^>]*>)|(?P<आयडेंटिफायर_मूल्य>[^\W\d]\w*)', re.S | re.M)

def रूपांतरकरा_मूल्य(स्रोत):
    def बदलावे_मूल्य(आहे_समान):
        if आहे_समान.lastgroup == '보존':
            return आहे_समान[0]
        return ''.join(वर्ण_मूल्य if ord(वर्ण_मूल्य) < 128 else
                       ('\\u%04x' if ord(वर्ण_मूल्य) <= 65535 else '\\U%08x') % ord(वर्ण_मूल्य)
                       for वर्ण_मूल्य in आहे_समान[0])
    return टोकन_मूल्य.sub(बदलावे_मूल्य, स्रोत)

def आज्ञा_कार्यवाही_करा():
    व्याकरणविश्लेषक_48ee4b1b = argparse.ArgumentParser()
    व्याकरणविश्लेषक_48ee4b1b.add_argument('मूळ', type=Path)
    व्याकरणविश्लेषक_48ee4b1b.add_argument('आउटपुट', type=Path)
    बाबी = व्याकरणविश्लेषक_48ee4b1b.parse_args()
    for फाइल in sorted(बाबी.मूळ.rglob('*')):
        if फाइल.suffix not in ('.c', '.h'):
            continue
        आउटपुट = बाबी.आउटपुट / फाइल.relative_to(बाबी.मूळ)
        आउटपुट.parent.mkdir(parents=True, exist_ok=True)
        नवे_स्रोत = रूपांतरकरा_मूल्य(फाइल.read_text())
        if not आउटपुट.exists() or आउटपुट.read_text() != नवे_स्रोत:
            आउटपुट.write_text(नवे_स्रोत)

if __name__ == '__main__':
    आज्ञा_कार्यवाही_करा()
