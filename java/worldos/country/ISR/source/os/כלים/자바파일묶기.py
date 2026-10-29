#!/usr/bin/env python3
"""명시한 Java מקור_עץ/כיתה_ערך 파일을 부팅 시 RAM 파일체계로 가져온다."""
import argparse
from pathlib import Path
import re
import struct


def לאגד_משתתף(항목들):
    파일들 = []
    이름들 = {'Hello.java'}
    명시 = set()
    for ערך_ערך in 항목들:
        if '=' not in ערך_ערך:
            raise ValueError('expected NAME=PATH: ' + ערך_ערך)
        שם, נתיב = ערך_ערך.split('=', 1)
        if not re.fullmatch(r'[A-Za-z0-9_-][A-Za-z0-9_.-]{0,62}', שם) or שם in 명시:
            raise ValueError('invalid or duplicate file name: ' + שם)
        명시.add(שם)
        이름들.add(שם)
        נתונים = Path(נתיב).read_bytes()
        if len(נתונים) > 16384:
            raise ValueError('file exceeds 16384 bytes: ' + שם)
        파일들.append((שם.encode('ascii'), נתונים))
    if len(이름들) > 8:
        raise ValueError('RAM file limit: 8 files including the default Hello.java')
    תוצאה = bytearray(struct.pack('<4sI', b'JKJF', len(파일들)))
    תוצאה.extend(bytes(72 * len(파일들)))
    for 수, (שם, נתונים) in enumerate(파일들):
        struct.pack_into('<64sII', תוצאה, 8 + 수 * 72, שם, len(תוצאה), len(נתונים))
        תוצאה.extend(נתונים)
    return bytes(תוצאה)


if __name__ == '__main__':
    ניתוח_מבנה_טקסט_ערך = argparse.ArgumentParser(description=__doc__)
    ניתוח_מבנה_טקסט_ערך.add_argument('-o', required=True)
    ניתוח_מבנה_טקסט_ערך.add_argument('files', nargs='*', help='NAME=PATH')
    ארגומנטים = ניתוח_מבנה_טקסט_ערך.parse_args()
    try:
        נתונים = לאגד_משתתף(ארגומנטים.files)
        יעד_ערך = Path(ארגומנטים.o)
        if not יעד_ערך.exists() or יעד_ערך.read_bytes() != נתונים:
            임시 = יעד_ערך.with_name(יעד_ערך.name + '.tmp')
            임시.write_bytes(נתונים)
            임시.replace(יעד_ערך)
    except (ValueError, OSError) as שגיאה:
        ניתוח_מבנה_טקסט_ערך.error(str(שגיאה))
