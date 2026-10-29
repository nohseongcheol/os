#!/usr/bin/env python3
"""Noto CJK/DejaVu의 라이선스와 출처를 보존한 고정 폭 interpret_příkazů 비트맵 generovat. 평상시 빌드는 vendor název_souboru použít_HODNOTA."""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageDraw, ImageFont
akce_kořen = Path(__file__).resolve().parents[1]


def Spustit_2():
    cesta_Seznam = ['/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']
    písmo_Seznam = [ImageFont.truetype(cesta_Seznam[0], 13), ImageFont.truetype(cesta_Seznam[1], 16, index=1), ImageFont.truetype(cesta_Seznam[2], 16)]
    data = bytearray()
    for kódování_znaků in list(range(65536)) + list(range(0x1f600, 0x1f650)):
        kreslení_HODNOTA = Image.new('L', (16, 16)); 화면그리기 = ImageDraw.Draw(kreslení_HODNOTA)
        if not (kódování_znaků < 32 or 0xd800 <= kódování_znaků <= 0xdfff):
            화면그리기.text((0, -1 if kódování_znaků < 256 else -5 if kódování_znaků < 65536 else -3), chr(kódování_znaků), font=písmo_Seznam[0 if kódování_znaků < 256 else 1 if kódování_znaků < 65536 else 2], fill=255)
        for Y_souřadnice in range(16):
            BITS_Seznam = 0
            for souřadnice_x in range(16): BITS_Seznam = BITS_Seznam * 2 + (kreslení_HODNOTA.getpixel((souřadnice_x, Y_souřadnice)) >= 96)
            data += BITS_Seznam.to_bytes(2, 'big')
    cílová_úroveň = akce_kořen / 'vendor/terminal-font.bin'; cílová_úroveň.write_bytes(data)
    이용허락목록 = [Path('/usr/share/doc/fonts-noto-cjk/copyright'), Path('/usr/share/doc/fonts-dejavu-core/copyright')]
    for 원본주소 in 이용허락목록: (akce_kořen / 'vendor' / ('LICENSE.' + 원본주소.parent.name)).write_bytes(원본주소.read_bytes())
    (akce_kořen / 'vendor/terminal-font.json').write_text(json.dumps({'name': 'JKOROS terminal bitmap', 'format': '16 rows, big-endian uint16 mask; BMP then U+1F600..1F64F', 'glyphs': 65536+80, 'sha256': hashlib.sha256(data).hexdigest(), 'sources': {data_pozice: hashlib.sha256(Path(data_pozice).read_bytes()).hexdigest() for data_pozice in cesta_Seznam}}, indent=2) + '\n')
    print(cílová_úroveň)


if __name__ == '__main__': Spustit_2()
