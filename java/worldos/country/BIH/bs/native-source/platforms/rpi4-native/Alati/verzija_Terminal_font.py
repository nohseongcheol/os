#!/usr/bin/env python3
"""Noto CJK/DejaVu의 라이선스와 출처를 보존한 고정 폭 Terminal 비트맵 generirati. 평상시 빌드는 vendor Fajl 사용."""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageDraw, ImageFont
projicirati_koijen = Path(__file__).resolve().parents[1]


def Pokreni():
    put_spisak = ['/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']
    font_spisak = [ImageFont.truetype(put_spisak[0], 13), ImageFont.truetype(put_spisak[1], 16, index=1), ImageFont.truetype(put_spisak[2], 16)]
    podaci = bytearray()
    for znak_kodiranje in list(range(65536)) + list(range(0x1f600, 0x1f650)):
        ucrtavanje_VALUE = Image.new('L', (16, 16)); 화면그리기 = ImageDraw.Draw(ucrtavanje_VALUE)
        if not (znak_kodiranje < 32 or 0xd800 <= znak_kodiranje <= 0xdfff):
            화면그리기.text((0, -1 if znak_kodiranje < 256 else -5 if znak_kodiranje < 65536 else -3), chr(znak_kodiranje), font=font_spisak[0 if znak_kodiranje < 256 else 1 if znak_kodiranje < 65536 else 2], fill=255)
        for Y_koordinata in range(16):
            비트들 = 0
            for koordinata_x in range(16): 비트들 = 비트들 * 2 + (ucrtavanje_VALUE.getpixel((koordinata_x, Y_koordinata)) >= 96)
            podaci += 비트들.to_bytes(2, 'big')
    cilj = projicirati_koijen / 'vendor/terminal-font.bin'; cilj.write_bytes(podaci)
    이용허락목록 = [Path('/usr/share/doc/fonts-noto-cjk/copyright'), Path('/usr/share/doc/fonts-dejavu-core/copyright')]
    for 원본주소 in 이용허락목록: (projicirati_koijen / 'vendor' / ('LICENSE.' + 원본주소.parent.name)).write_bytes(원본주소.read_bytes())
    (projicirati_koijen / 'vendor/terminal-font.json').write_text(json.dumps({'name': 'JKOROS terminal bitmap', 'format': '16 rows, big-endian uint16 mask; BMP then U+1F600..1F64F', 'glyphs': 65536+80, 'sha256': hashlib.sha256(podaci).hexdigest(), 'sources': {podaci_položaj: hashlib.sha256(Path(podaci_položaj).read_bytes()).hexdigest() for podaci_položaj in put_spisak}}, indent=2) + '\n')
    print(cilj)


if __name__ == '__main__': Pokreni()
