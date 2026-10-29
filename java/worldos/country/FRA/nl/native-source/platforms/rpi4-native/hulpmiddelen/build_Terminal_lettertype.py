#!/usr/bin/env python3
"""Noto CJK/DejaVu의 라이선스와 출처를 보존한 고정 폭 terminal 비트맵 genereren. 평상시 빌드는 vendor bestand gebruik_WAARDE."""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageDraw, ImageFont
Taken_wortel = Path(__file__).resolve().parents[1]


def starten():
    pad_Lijst = ['/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']
    lettertype_Lijst = [ImageFont.truetype(pad_Lijst[0], 13), ImageFont.truetype(pad_Lijst[1], 16, index=1), ImageFont.truetype(pad_Lijst[2], 16)]
    gegevens = bytearray()
    for tekencodering in list(range(65536)) + list(range(0x1f600, 0x1f650)):
        tekening_WAARDE = Image.new('L', (16, 16)); Tekenen_scherm = ImageDraw.Draw(tekening_WAARDE)
        if not (tekencodering < 32 or 0xd800 <= tekencodering <= 0xdfff):
            Tekenen_scherm.text((0, -1 if tekencodering < 256 else -5 if tekencodering < 65536 else -3), chr(tekencodering), font=lettertype_Lijst[0 if tekencodering < 256 else 1 if tekencodering < 65536 else 2], fill=255)
        for Y_coördinaat in range(16):
            BITS_Lijst = 0
            for x_coördinaat in range(16): BITS_Lijst = BITS_Lijst * 2 + (tekening_WAARDE.getpixel((x_coördinaat, Y_coördinaat)) >= 96)
            gegevens += BITS_Lijst.to_bytes(2, 'big')
    doel = Taken_wortel / 'vendor/terminal-font.bin'; doel.write_bytes(gegevens)
    이용허락목록 = [Path('/usr/share/doc/fonts-noto-cjk/copyright'), Path('/usr/share/doc/fonts-dejavu-core/copyright')]
    for 원본주소 in 이용허락목록: (Taken_wortel / 'vendor' / ('LICENSE.' + 원본주소.parent.name)).write_bytes(원본주소.read_bytes())
    (Taken_wortel / 'vendor/terminal-font.json').write_text(json.dumps({'name': 'JKOROS terminal bitmap', 'format': '16 rows, big-endian uint16 mask; BMP then U+1F600..1F64F', 'glyphs': 65536+80, 'sha256': hashlib.sha256(gegevens).hexdigest(), 'sources': {gegevens_functie: hashlib.sha256(Path(gegevens_functie).read_bytes()).hexdigest() for gegevens_functie in pad_Lijst}}, indent=2) + '\n')
    print(doel)


if __name__ == '__main__': starten()
