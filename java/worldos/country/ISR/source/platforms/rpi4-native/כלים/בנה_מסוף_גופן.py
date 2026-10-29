#!/usr/bin/env python3
"""Noto CJK/DejaVu의 라이선스와 출처를 보존한 고정 폭 מסוף 비트맵 יצר. 평상시 빌드는 vendor קובץ שימוש_ערך."""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageDraw, ImageFont
לשקף_בסיס = Path(__file__).resolve().parents[1]


def הפעלה():
    נתיב_רשימה = ['/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']
    גופן_רשימה = [ImageFont.truetype(נתיב_רשימה[0], 13), ImageFont.truetype(נתיב_רשימה[1], 16, index=1), ImageFont.truetype(נתיב_רשימה[2], 16)]
    נתונים = bytearray()
    for תו_קידוד in list(range(65536)) + list(range(0x1f600, 0x1f650)):
        ציור_ערך = Image.new('L', (16, 16)); 화면그리기 = ImageDraw.Draw(ציור_ערך)
        if not (תו_קידוד < 32 or 0xd800 <= תו_קידוד <= 0xdfff):
            화면그리기.text((0, -1 if תו_קידוד < 256 else -5 if תו_קידוד < 65536 else -3), chr(תו_קידוד), font=גופן_רשימה[0 if תו_קידוד < 256 else 1 if תו_קידוד < 65536 else 2], fill=255)
        for 세로좌표 in range(16):
            비트들 = 0
            for קואורדינטת_x in range(16): 비트들 = 비트들 * 2 + (ציור_ערך.getpixel((קואורדינטת_x, 세로좌표)) >= 96)
            נתונים += 비트들.to_bytes(2, 'big')
    יעד = לשקף_בסיס / 'vendor/terminal-font.bin'; יעד.write_bytes(נתונים)
    이용허락목록 = [Path('/usr/share/doc/fonts-noto-cjk/copyright'), Path('/usr/share/doc/fonts-dejavu-core/copyright')]
    for 원본주소 in 이용허락목록: (לשקף_בסיס / 'vendor' / ('LICENSE.' + 원본주소.parent.name)).write_bytes(원본주소.read_bytes())
    (לשקף_בסיס / 'vendor/terminal-font.json').write_text(json.dumps({'name': 'JKOROS terminal bitmap', 'format': '16 rows, big-endian uint16 mask; BMP then U+1F600..1F64F', 'glyphs': 65536+80, 'sha256': hashlib.sha256(נתונים).hexdigest(), 'sources': {נתונים_עמדה: hashlib.sha256(Path(נתונים_עמדה).read_bytes()).hexdigest() for נתונים_עמדה in נתיב_רשימה}}, indent=2) + '\n')
    print(יעד)


if __name__ == '__main__': הפעלה()
