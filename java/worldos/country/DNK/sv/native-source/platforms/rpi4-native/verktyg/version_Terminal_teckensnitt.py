#!/usr/bin/env python3
"""Noto CJK/DejaVu의 라이선스와 출처를 보존한 고정 폭 kommandotolk 비트맵 generera. 평상시 빌드는 vendor filnamn använda_värde."""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageDraw, ImageFont
åtgärd_rot = Path(__file__).resolve().parents[1]


def Kör():
    väg_ange = ['/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']
    teckensnitt_ange = [ImageFont.truetype(väg_ange[0], 13), ImageFont.truetype(väg_ange[1], 16, index=1), ImageFont.truetype(väg_ange[2], 16)]
    data = bytearray()
    for teckenkodning in list(range(65536)) + list(range(0x1f600, 0x1f650)):
        ritning_värde = Image.new('L', (16, 16)); Rita_skärmbild = ImageDraw.Draw(ritning_värde)
        if not (teckenkodning < 32 or 0xd800 <= teckenkodning <= 0xdfff):
            Rita_skärmbild.text((0, -1 if teckenkodning < 256 else -5 if teckenkodning < 65536 else -3), chr(teckenkodning), font=teckensnitt_ange[0 if teckenkodning < 256 else 1 if teckenkodning < 65536 else 2], fill=255)
        for Y_koordinat in range(16):
            BITS_ange = 0
            for x_koordinat in range(16): BITS_ange = BITS_ange * 2 + (ritning_värde.getpixel((x_koordinat, Y_koordinat)) >= 96)
            data += BITS_ange.to_bytes(2, 'big')
    mål = åtgärd_rot / 'vendor/terminal-font.bin'; mål.write_bytes(data)
    이용허락목록 = [Path('/usr/share/doc/fonts-noto-cjk/copyright'), Path('/usr/share/doc/fonts-dejavu-core/copyright')]
    for 원본주소 in 이용허락목록: (åtgärd_rot / 'vendor' / ('LICENSE.' + 원본주소.parent.name)).write_bytes(원본주소.read_bytes())
    (åtgärd_rot / 'vendor/terminal-font.json').write_text(json.dumps({'name': 'JKOROS terminal bitmap', 'format': '16 rows, big-endian uint16 mask; BMP then U+1F600..1F64F', 'glyphs': 65536+80, 'sha256': hashlib.sha256(data).hexdigest(), 'sources': {data_placera: hashlib.sha256(Path(data_placera).read_bytes()).hexdigest() for data_placera in väg_ange}}, indent=2) + '\n')
    print(mål)


if __name__ == '__main__': Kör()
