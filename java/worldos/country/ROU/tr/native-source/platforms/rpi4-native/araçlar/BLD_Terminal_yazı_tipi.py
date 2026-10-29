#!/usr/bin/env python3
"""Noto CJK/DejaVu의 라이선스와 출처를 보존한 고정 폭 uçbirim 비트맵 oluşturmak. 평상시 빌드는 vendor dosya kullanmak_değer."""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageDraw, ImageFont
işlem_kök = Path(__file__).resolve().parents[1]


def çalıştır():
    yol_Liste = ['/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']
    yazı_tipi_Liste = [ImageFont.truetype(yol_Liste[0], 13), ImageFont.truetype(yol_Liste[1], 16, index=1), ImageFont.truetype(yol_Liste[2], 16)]
    veri = bytearray()
    for karakter_kodlaması in list(range(65536)) + list(range(0x1f600, 0x1f650)):
        çizim_değer = Image.new('L', (16, 16)); 화면그리기 = ImageDraw.Draw(çizim_değer)
        if not (karakter_kodlaması < 32 or 0xd800 <= karakter_kodlaması <= 0xdfff):
            화면그리기.text((0, -1 if karakter_kodlaması < 256 else -5 if karakter_kodlaması < 65536 else -3), chr(karakter_kodlaması), font=yazı_tipi_Liste[0 if karakter_kodlaması < 256 else 1 if karakter_kodlaması < 65536 else 2], fill=255)
        for Y_koordinat in range(16):
            BITS_Liste = 0
            for x_koordinatı in range(16): BITS_Liste = BITS_Liste * 2 + (çizim_değer.getpixel((x_koordinatı, Y_koordinat)) >= 96)
            veri += BITS_Liste.to_bytes(2, 'big')
    hedef = işlem_kök / 'vendor/terminal-font.bin'; hedef.write_bytes(veri)
    이용허락목록 = [Path('/usr/share/doc/fonts-noto-cjk/copyright'), Path('/usr/share/doc/fonts-dejavu-core/copyright')]
    for 원본주소 in 이용허락목록: (işlem_kök / 'vendor' / ('LICENSE.' + 원본주소.parent.name)).write_bytes(원본주소.read_bytes())
    (işlem_kök / 'vendor/terminal-font.json').write_text(json.dumps({'name': 'JKOROS terminal bitmap', 'format': '16 rows, big-endian uint16 mask; BMP then U+1F600..1F64F', 'glyphs': 65536+80, 'sha256': hashlib.sha256(veri).hexdigest(), 'sources': {veri_konum: hashlib.sha256(Path(veri_konum).read_bytes()).hexdigest() for veri_konum in yol_Liste}}, indent=2) + '\n')
    print(hedef)


if __name__ == '__main__': çalıştır()
