#!/usr/bin/env python3
"""Noto CJK/DejaVu의 라이선스와 출처를 보존한 고정 폭 Terminaal 비트맵 genereer. 평상시 빌드는 vendor Lêer 사용."""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageDraw, ImageFont
Project_wortel = Path(__file__).resolve().parents[1]


def Loop():
    pad_Lys = ['/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']
    font_Lys = [ImageFont.truetype(pad_Lys[0], 13), ImageFont.truetype(pad_Lys[1], 16, index=1), ImageFont.truetype(pad_Lys[2], 16)]
    data = bytearray()
    for karakter_enkodering in list(range(65536)) + list(range(0x1f600, 0x1f650)):
        tekening_VALUE = Image.new('L', (16, 16)); 화면그리기 = ImageDraw.Draw(tekening_VALUE)
        if not (karakter_enkodering < 32 or 0xd800 <= karakter_enkodering <= 0xdfff):
            화면그리기.text((0, -1 if karakter_enkodering < 256 else -5 if karakter_enkodering < 65536 else -3), chr(karakter_enkodering), font=font_Lys[0 if karakter_enkodering < 256 else 1 if karakter_enkodering < 65536 else 2], fill=255)
        for Y_koördinaat in range(16):
            Agtergrond_intelligente_oordragdiens_Lys = 0
            for x_koördinaat in range(16): Agtergrond_intelligente_oordragdiens_Lys = Agtergrond_intelligente_oordragdiens_Lys * 2 + (tekening_VALUE.getpixel((x_koördinaat, Y_koördinaat)) >= 96)
            data += Agtergrond_intelligente_oordragdiens_Lys.to_bytes(2, 'big')
    teiken = Project_wortel / 'vendor/terminal-font.bin'; teiken.write_bytes(data)
    이용허락목록 = [Path('/usr/share/doc/fonts-noto-cjk/copyright'), Path('/usr/share/doc/fonts-dejavu-core/copyright')]
    for 원본주소 in 이용허락목록: (Project_wortel / 'vendor' / ('LICENSE.' + 원본주소.parent.name)).write_bytes(원본주소.read_bytes())
    (Project_wortel / 'vendor/terminal-font.json').write_text(json.dumps({'name': 'JKOROS terminal bitmap', 'format': '16 rows, big-endian uint16 mask; BMP then U+1F600..1F64F', 'glyphs': 65536+80, 'sha256': hashlib.sha256(data).hexdigest(), 'sources': {data_plaas: hashlib.sha256(Path(data_plaas).read_bytes()).hexdigest() for data_plaas in pad_Lys}}, indent=2) + '\n')
    print(teiken)


if __name__ == '__main__': Loop()
