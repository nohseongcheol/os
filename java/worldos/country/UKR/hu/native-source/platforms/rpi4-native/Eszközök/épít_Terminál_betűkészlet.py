#!/usr/bin/env python3
"""Noto CJK/DejaVu의 라이선스와 출처를 보존한 고정 폭 Terminál 비트맵 generálás. 평상시 빌드는 vendor Fájl használ_ÉRTÉK."""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageDraw, ImageFont
teendő_gyök = Path(__file__).resolve().parents[1]


def Futtatás():
    útvonal_Lista = ['/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']
    betűkészlet_Lista = [ImageFont.truetype(útvonal_Lista[0], 13), ImageFont.truetype(útvonal_Lista[1], 16, index=1), ImageFont.truetype(útvonal_Lista[2], 16)]
    adat = bytearray()
    for karakterkódolás in list(range(65536)) + list(range(0x1f600, 0x1f650)):
        rajz_ÉRTÉK = Image.new('L', (16, 16)); 화면그리기 = ImageDraw.Draw(rajz_ÉRTÉK)
        if not (karakterkódolás < 32 or 0xd800 <= karakterkódolás <= 0xdfff):
            화면그리기.text((0, -1 if karakterkódolás < 256 else -5 if karakterkódolás < 65536 else -3), chr(karakterkódolás), font=betűkészlet_Lista[0 if karakterkódolás < 256 else 1 if karakterkódolás < 65536 else 2], fill=255)
        for Y_koordináta in range(16):
            BITS_Lista = 0
            for x_koordináta in range(16): BITS_Lista = BITS_Lista * 2 + (rajz_ÉRTÉK.getpixel((x_koordináta, Y_koordináta)) >= 96)
            adat += BITS_Lista.to_bytes(2, 'big')
    cél = teendő_gyök / 'vendor/terminal-font.bin'; cél.write_bytes(adat)
    이용허락목록 = [Path('/usr/share/doc/fonts-noto-cjk/copyright'), Path('/usr/share/doc/fonts-dejavu-core/copyright')]
    for 원본주소 in 이용허락목록: (teendő_gyök / 'vendor' / ('LICENSE.' + 원본주소.parent.name)).write_bytes(원본주소.read_bytes())
    (teendő_gyök / 'vendor/terminal-font.json').write_text(json.dumps({'name': 'JKOROS terminal bitmap', 'format': '16 rows, big-endian uint16 mask; BMP then U+1F600..1F64F', 'glyphs': 65536+80, 'sha256': hashlib.sha256(adat).hexdigest(), 'sources': {adat_pozíció: hashlib.sha256(Path(adat_pozíció).read_bytes()).hexdigest() for adat_pozíció in útvonal_Lista}}, indent=2) + '\n')
    print(cél)


if __name__ == '__main__': Futtatás()
