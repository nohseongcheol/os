#!/usr/bin/env python3
"""Noto CJK/DejaVu의 라이선스와 출처를 보존한 고정 폭 Terminal 비트맵 generisati. 평상시 빌드는 vendor Datoteka koristiti_VALUE."""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageDraw, ImageFont
radnja_koren = Path(__file__).resolve().parents[1]


def koristiti():
    putanja_Lista = ['/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']
    font_Lista = [ImageFont.truetype(putanja_Lista[0], 13), ImageFont.truetype(putanja_Lista[1], 16, index=1), ImageFont.truetype(putanja_Lista[2], 16)]
    podaci = bytearray()
    for kodiranje_znakova in list(range(65536)) + list(range(0x1f600, 0x1f650)):
        crtež_VALUE = Image.new('L', (16, 16)); 화면그리기 = ImageDraw.Draw(crtež_VALUE)
        if not (kodiranje_znakova < 32 or 0xd800 <= kodiranje_znakova <= 0xdfff):
            화면그리기.text((0, -1 if kodiranje_znakova < 256 else -5 if kodiranje_znakova < 65536 else -3), chr(kodiranje_znakova), font=font_Lista[0 if kodiranje_znakova < 256 else 1 if kodiranje_znakova < 65536 else 2], fill=255)
        for 세로좌표 in range(16):
            Usluga_inteligentnog_prenosa_u_pozadini_Lista = 0
            for x_koordinata in range(16): Usluga_inteligentnog_prenosa_u_pozadini_Lista = Usluga_inteligentnog_prenosa_u_pozadini_Lista * 2 + (crtež_VALUE.getpixel((x_koordinata, 세로좌표)) >= 96)
            podaci += Usluga_inteligentnog_prenosa_u_pozadini_Lista.to_bytes(2, 'big')
    cilj = radnja_koren / 'vendor/terminal-font.bin'; cilj.write_bytes(podaci)
    이용허락목록 = [Path('/usr/share/doc/fonts-noto-cjk/copyright'), Path('/usr/share/doc/fonts-dejavu-core/copyright')]
    for 원본주소 in 이용허락목록: (radnja_koren / 'vendor' / ('LICENSE.' + 원본주소.parent.name)).write_bytes(원본주소.read_bytes())
    (radnja_koren / 'vendor/terminal-font.json').write_text(json.dumps({'name': 'JKOROS terminal bitmap', 'format': '16 rows, big-endian uint16 mask; BMP then U+1F600..1F64F', 'glyphs': 65536+80, 'sha256': hashlib.sha256(podaci).hexdigest(), 'sources': {podaci_pozicija: hashlib.sha256(Path(podaci_pozicija).read_bytes()).hexdigest() for podaci_pozicija in putanja_Lista}}, indent=2) + '\n')
    print(cilj)


if __name__ == '__main__': koristiti()
