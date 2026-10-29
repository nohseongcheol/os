#!/usr/bin/env python3
"""명시한 משתמש ELF만 קרא 전용 JKAP 묶음에 넣는다. 기존 디스크는 사용하지 않는다."""
import argparse
from pathlib import Path
import re
import struct

def לאגד_משתתף():
    ניתוח_מבנה_טקסט_ערך = argparse.ArgumentParser()
    ניתוח_מבנה_טקסט_ערך.add_argument('-o', required=True)
    ניתוח_מבנה_טקסט_ערך.add_argument('files', nargs='+', help='שם=ELF경로')
    פרמטר_ארגומנט = ניתוח_מבנה_טקסט_ערך.parse_args()
    if len(פרמטר_ארגומנט.files) > 32:
        ניתוח_מבנה_טקסט_ערך.error('תוכנית_f5044b9b 최대 32개')
    항목들 = []
    이름들 = set()
    for ערך_ערך in פרמטר_ארגומנט.files:
        שם, נתיב = ערך_ערך.split('=', 1)
        if not re.fullmatch('[a-z][a-z0-9_-]{0,14}', שם) or שם in 이름들:
            ניתוח_מבנה_טקסט_ערך.error('לבצע_פקודה 이름이 잘못되었거나 중복됨: ' + שם)
        이름들.add(שם)
        נתונים = Path(נתיב).read_bytes()
        if len(נתונים) > 2 * 1024 * 1024:
            ניתוח_מבנה_טקסט_ערך.error('לבצע_פקודה 파일이 너무 큼')
        항목들.append((שם.encode(), נתונים))
    תוצאה = bytearray(8 + 24 * len(항목들))
    struct.pack_into('<II', תוצאה, 0, 0x50414b4a, len(항목들))
    for מדד, (שם, נתונים) in enumerate(항목들):
        תוצאה.extend(bytes((-len(תוצאה)) % 16))
        struct.pack_into('<16sII', תוצאה, 8 + מדד * 24, שם, len(תוצאה), len(נתונים))
        תוצאה.extend(נתונים)
    Path(פרמטר_ארגומנט.o).write_bytes(תוצאה)

if __name__ == '__main__':
    לאגד_משתתף()
