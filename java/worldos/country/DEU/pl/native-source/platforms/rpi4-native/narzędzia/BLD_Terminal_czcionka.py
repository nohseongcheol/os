#!/usr/bin/env python3
"""Noto CJK/DejaVu의 라이선스와 출처를 보존한 고정 폭 interpretator_poleceń 비트맵 generować. 평상시 빌드는 vendor nazwa_pliku używać_WARTOŚĆ."""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageDraw, ImageFont
Project_korzeń = Path(__file__).resolve().parents[1]


def Uruchom_2():
    ścieżka_Lista = ['/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']
    czcionka_Lista = [ImageFont.truetype(ścieżka_Lista[0], 13), ImageFont.truetype(ścieżka_Lista[1], 16, index=1), ImageFont.truetype(ścieżka_Lista[2], 16)]
    dane = bytearray()
    for kodowanie_znaku in list(range(65536)) + list(range(0x1f600, 0x1f650)):
        rysunek_WARTOŚĆ = Image.new('L', (16, 16)); 화면그리기 = ImageDraw.Draw(rysunek_WARTOŚĆ)
        if not (kodowanie_znaku < 32 or 0xd800 <= kodowanie_znaku <= 0xdfff):
            화면그리기.text((0, -1 if kodowanie_znaku < 256 else -5 if kodowanie_znaku < 65536 else -3), chr(kodowanie_znaku), font=czcionka_Lista[0 if kodowanie_znaku < 256 else 1 if kodowanie_znaku < 65536 else 2], fill=255)
        for Y_współrzędna in range(16):
            BITS_Lista = 0
            for współrzędna_X in range(16): BITS_Lista = BITS_Lista * 2 + (rysunek_WARTOŚĆ.getpixel((współrzędna_X, Y_współrzędna)) >= 96)
            dane += BITS_Lista.to_bytes(2, 'big')
    wartość_docelowa = Project_korzeń / 'vendor/terminal-font.bin'; wartość_docelowa.write_bytes(dane)
    이용허락목록 = [Path('/usr/share/doc/fonts-noto-cjk/copyright'), Path('/usr/share/doc/fonts-dejavu-core/copyright')]
    for 원본주소 in 이용허락목록: (Project_korzeń / 'vendor' / ('LICENSE.' + 원본주소.parent.name)).write_bytes(원본주소.read_bytes())
    (Project_korzeń / 'vendor/terminal-font.json').write_text(json.dumps({'name': 'JKOROS terminal bitmap', 'format': '16 rows, big-endian uint16 mask; BMP then U+1F600..1F64F', 'glyphs': 65536+80, 'sha256': hashlib.sha256(dane).hexdigest(), 'sources': {dane_stanowisko: hashlib.sha256(Path(dane_stanowisko).read_bytes()).hexdigest() for dane_stanowisko in ścieżka_Lista}}, indent=2) + '\n')
    print(wartość_docelowa)


if __name__ == '__main__': Uruchom_2()
