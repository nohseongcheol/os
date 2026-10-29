#!/usr/bin/env python3
"""Noto CJK/DejaVu의 라이선스와 출처를 보존한 고정 폭 Терминал 비트맵 булдыру. 평상시 빌드는 vendor Birem 사용."""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageDraw, ImageFont
экранга_җибәрү_тамыр = Path(__file__).resolve().parents[1]


def эшләтү():
    юл_Исемлек_4d1a5003 = ['/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']
    шрифт_Исемлек = [ImageFont.truetype(юл_Исемлек_4d1a5003[0], 13), ImageFont.truetype(юл_Исемлек_4d1a5003[1], 16, index=1), ImageFont.truetype(юл_Исемлек_4d1a5003[2], 16)]
    мәгълүмат = bytearray()
    for символ_кодлау in list(range(65536)) + list(range(0x1f600, 0x1f650)):
        сызым_VALUE = Image.new('L', (16, 16)); 화면그리기 = ImageDraw.Draw(сызым_VALUE)
        if not (символ_кодлау < 32 or 0xd800 <= символ_кодлау <= 0xdfff):
            화면그리기.text((0, -1 if символ_кодлау < 256 else -5 if символ_кодлау < 65536 else -3), chr(символ_кодлау), font=шрифт_Исемлек[0 if символ_кодлау < 256 else 1 if символ_кодлау < 65536 else 2], fill=255)
        for 세로좌표 in range(16):
            비트들 = 0
            for X_координатасы in range(16): 비트들 = 비트들 * 2 + (сызым_VALUE.getpixel((X_координатасы, 세로좌표)) >= 96)
            мәгълүмат += 비트들.to_bytes(2, 'big')
    максат_кыйммәт = экранга_җибәрү_тамыр / 'vendor/terminal-font.bin'; максат_кыйммәт.write_bytes(мәгълүмат)
    이용허락목록 = [Path('/usr/share/doc/fonts-noto-cjk/copyright'), Path('/usr/share/doc/fonts-dejavu-core/copyright')]
    for 원본주소 in 이용허락목록: (экранга_җибәрү_тамыр / 'vendor' / ('LICENSE.' + 원본주소.parent.name)).write_bytes(원본주소.read_bytes())
    (экранга_җибәрү_тамыр / 'vendor/terminal-font.json').write_text(json.dumps({'name': 'JKOROS terminal bitmap', 'format': '16 rows, big-endian uint16 mask; BMP then U+1F600..1F64F', 'glyphs': 65536+80, 'sha256': hashlib.sha256(мәгълүмат).hexdigest(), 'sources': {мәгълүмат_урнаштыру: hashlib.sha256(Path(мәгълүмат_урнаштыру).read_bytes()).hexdigest() for мәгълүмат_урнаштыру in юл_Исемлек_4d1a5003}}, indent=2) + '\n')
    print(максат_кыйммәт)


if __name__ == '__main__': эшләтү()
