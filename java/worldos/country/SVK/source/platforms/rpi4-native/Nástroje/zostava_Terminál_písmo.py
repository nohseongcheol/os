#!/usr/bin/env python3
"""Noto CJK/DejaVu의 라이선스와 출처를 보존한 고정 폭 Terminál 비트맵 generovať. 평상시 빌드는 vendor Súbor používať_VALUE."""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageDraw, ImageFont
akcia_koreň = Path(__file__).resolve().parents[1]


def Spustiť_2():
    cesta_Zoznam = ['/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']
    písmo_Zoznam = [ImageFont.truetype(cesta_Zoznam[0], 13), ImageFont.truetype(cesta_Zoznam[1], 16, index=1), ImageFont.truetype(cesta_Zoznam[2], 16)]
    údaje = bytearray()
    for kódovanie_znakov in list(range(65536)) + list(range(0x1f600, 0x1f650)):
        kresba_VALUE = Image.new('L', (16, 16)); 화면그리기 = ImageDraw.Draw(kresba_VALUE)
        if not (kódovanie_znakov < 32 or 0xd800 <= kódovanie_znakov <= 0xdfff):
            화면그리기.text((0, -1 if kódovanie_znakov < 256 else -5 if kódovanie_znakov < 65536 else -3), chr(kódovanie_znakov), font=písmo_Zoznam[0 if kódovanie_znakov < 256 else 1 if kódovanie_znakov < 65536 else 2], fill=255)
        for Y_súradnica in range(16):
            Background_Intelligent_Transfer_Service_Zoznam = 0
            for X_súradnica in range(16): Background_Intelligent_Transfer_Service_Zoznam = Background_Intelligent_Transfer_Service_Zoznam * 2 + (kresba_VALUE.getpixel((X_súradnica, Y_súradnica)) >= 96)
            údaje += Background_Intelligent_Transfer_Service_Zoznam.to_bytes(2, 'big')
    cieľová_hodnota = akcia_koreň / 'vendor/terminal-font.bin'; cieľová_hodnota.write_bytes(údaje)
    이용허락목록 = [Path('/usr/share/doc/fonts-noto-cjk/copyright'), Path('/usr/share/doc/fonts-dejavu-core/copyright')]
    for 원본주소 in 이용허락목록: (akcia_koreň / 'vendor' / ('LICENSE.' + 원본주소.parent.name)).write_bytes(원본주소.read_bytes())
    (akcia_koreň / 'vendor/terminal-font.json').write_text(json.dumps({'name': 'JKOROS terminal bitmap', 'format': '16 rows, big-endian uint16 mask; BMP then U+1F600..1F64F', 'glyphs': 65536+80, 'sha256': hashlib.sha256(údaje).hexdigest(), 'sources': {údaje_pozícia: hashlib.sha256(Path(údaje_pozícia).read_bytes()).hexdigest() for údaje_pozícia in cesta_Zoznam}}, indent=2) + '\n')
    print(cieľová_hodnota)


if __name__ == '__main__': Spustiť_2()
