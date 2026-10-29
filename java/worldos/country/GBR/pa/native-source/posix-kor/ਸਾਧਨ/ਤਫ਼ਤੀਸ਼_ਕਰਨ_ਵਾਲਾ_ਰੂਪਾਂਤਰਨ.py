#!/usr/bin/env python3
"""ਪੰਜਾਬੀ C 식별자만 UCN으로 옮긴다. ਨਿਰਭਰ_ਰਹਿਣ_ਵਾਲਾ_ਕੀਮਤ·문자·주석·include 파일명은 보존한다."""
import argparse
from pathlib import Path
import re

ਟੋਕਨ_ਕੀਮਤ = re.compile(r'(?P<보존>//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|^[ \t]*#[ \t]*include[ \t]*<[^>]*>)|(?P<ਤਫ਼ਤੀਸ਼_ਕਰਨ_ਵਾਲਾ_ਕੀਮਤ>[^\W\d]\w*)', re.S | re.M)

def 변환(ਸਰੋਤ):
    def ਸਥਾਨ_ਬਦਲੋ_ਕੀਮਤ(일치):
        if 일치.lastgroup == '보존':
            return 일치[0]
        return ''.join(ਵਰਣ_ਕੀਮਤ if ord(ਵਰਣ_ਕੀਮਤ) < 128 else
                       ('\\u%04x' if ord(ਵਰਣ_ਕੀਮਤ) <= 65535 else '\\U%08x') % ord(ਵਰਣ_ਕੀਮਤ)
                       for ਵਰਣ_ਕੀਮਤ in 일치[0])
    return ਟੋਕਨ_ਕੀਮਤ.sub(ਸਥਾਨ_ਬਦਲੋ_ਕੀਮਤ, ਸਰੋਤ)

def ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼():
    해석기 = argparse.ArgumentParser()
    해석기.add_argument('원본', type=Path)
    해석기.add_argument('ਆਉਟਪੁੱਟ', type=Path)
    ਆਰਗੂਮੈਂਟ = 해석기.parse_args()
    for ਫਾਇਲ in sorted(ਆਰਗੂਮੈਂਟ.원본.rglob('*')):
        if ਫਾਇਲ.suffix not in ('.c', '.h'):
            continue
        ਆਉਟਪੁੱਟ = ਆਰਗੂਮੈਂਟ.ਆਉਟਪੁੱਟ / ਫਾਇਲ.relative_to(ਆਰਗੂਮੈਂਟ.원본)
        ਆਉਟਪੁੱਟ.parent.mkdir(parents=True, exist_ok=True)
        새원문 = 변환(ਫਾਇਲ.read_text())
        if not ਆਉਟਪੁੱਟ.exists() or ਆਉਟਪੁੱਟ.read_text() != 새원문:
            ਆਉਟਪੁੱਟ.write_text(새원문)

if __name__ == '__main__':
    ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼()
