#!/usr/bin/env python3
"""Noto CJK/DejaVu의 라이선스와 출처를 보존한 고정 폭 Terminal 비트맵 genera. 평상시 빌드는 vendor Fișier utiliza_VALUE."""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageDraw, ImageFont
Project_rădăcină = Path(__file__).resolve().parents[1]


def Pornește():
    cale_Listă = ['/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']
    font_Listă = [ImageFont.truetype(cale_Listă[0], 13), ImageFont.truetype(cale_Listă[1], 16, index=1), ImageFont.truetype(cale_Listă[2], 16)]
    date = bytearray()
    for codificare_caractere in list(range(65536)) + list(range(0x1f600, 0x1f650)):
        desen_VALUE = Image.new('L', (16, 16)); 화면그리기 = ImageDraw.Draw(desen_VALUE)
        if not (codificare_caractere < 32 or 0xd800 <= codificare_caractere <= 0xdfff):
            화면그리기.text((0, -1 if codificare_caractere < 256 else -5 if codificare_caractere < 65536 else -3), chr(codificare_caractere), font=font_Listă[0 if codificare_caractere < 256 else 1 if codificare_caractere < 65536 else 2], fill=255)
        for 세로좌표 in range(16):
            Serviciu_de_transfer_inteligent_în_fundal_Listă = 0
            for coordonata_X in range(16): Serviciu_de_transfer_inteligent_în_fundal_Listă = Serviciu_de_transfer_inteligent_în_fundal_Listă * 2 + (desen_VALUE.getpixel((coordonata_X, 세로좌표)) >= 96)
            date += Serviciu_de_transfer_inteligent_în_fundal_Listă.to_bytes(2, 'big')
    țintă = Project_rădăcină / 'vendor/terminal-font.bin'; țintă.write_bytes(date)
    이용허락목록 = [Path('/usr/share/doc/fonts-noto-cjk/copyright'), Path('/usr/share/doc/fonts-dejavu-core/copyright')]
    for 원본주소 in 이용허락목록: (Project_rădăcină / 'vendor' / ('LICENSE.' + 원본주소.parent.name)).write_bytes(원본주소.read_bytes())
    (Project_rădăcină / 'vendor/terminal-font.json').write_text(json.dumps({'name': 'JKOROS terminal bitmap', 'format': '16 rows, big-endian uint16 mask; BMP then U+1F600..1F64F', 'glyphs': 65536+80, 'sha256': hashlib.sha256(date).hexdigest(), 'sources': {date_poziție: hashlib.sha256(Path(date_poziție).read_bytes()).hexdigest() for date_poziție in cale_Listă}}, indent=2) + '\n')
    print(țintă)


if __name__ == '__main__': Pornește()
