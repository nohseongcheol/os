#!/usr/bin/env python3
"""한국어 C 식별자만 UCN으로 옮긴다. అక్షరసరం_మూల్యం·문자·주석·include 파일명은 보존한다."""
import argparse
from pathlib import Path
import re

టోకెన్_మూల్యం = re.compile(r'(?P<보존>//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|^[ \t]*#[ \t]*include[ \t]*<[^>]*>)|(?P<ఐడెంటిఫయర్_మూల్యం>[^\W\d]\w*)', re.S | re.M)

def 변환(వనరు):
    def మళ్లీ_పెట్టు_మూల్యం(일치):
        if 일치.lastgroup == '보존':
            return 일치[0]
        return ''.join(అక్షరం_మూల్యం if ord(అక్షరం_మూల్యం) < 128 else
                       ('\\u%04x' if ord(అక్షరం_మూల్యం) <= 65535 else '\\U%08x') % ord(అక్షరం_మూల్యం)
                       for అక్షరం_మూల్యం in 일치[0])
    return టోకెన్_మూల్యం.sub(మళ్లీ_పెట్టు_మూల్యం, వనరు)

def అమలు_చేయి_ఆదేశం():
    పార్సర్_48ee4b1b = argparse.ArgumentParser()
    పార్సర్_48ee4b1b.add_argument('원본', type=Path)
    పార్సర్_48ee4b1b.add_argument('అవుట్పుట్', type=Path)
    인수 = పార్సర్_48ee4b1b.parse_args()
    for దస్త్రం in sorted(인수.원본.rglob('*')):
        if దస్త్రం.suffix not in ('.c', '.h'):
            continue
        అవుట్పుట్ = 인수.అవుట్పుట్ / దస్త్రం.relative_to(인수.원본)
        అవుట్పుట్.parent.mkdir(parents=True, exist_ok=True)
        새원문 = 변환(దస్త్రం.read_text())
        if not అవుట్పుట్.exists() or అవుట్పుట్.read_text() != 새원문:
            అవుట్పుట్.write_text(새원문)

if __name__ == '__main__':
    అమలు_చేయి_ఆదేశం()
