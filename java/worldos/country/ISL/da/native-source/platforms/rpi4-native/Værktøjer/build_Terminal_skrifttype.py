#!/usr/bin/env python3
"""Noto CJK/DejaVu의 라이선스와 출처를 보존한 고정 폭 Terminal 비트맵 generere. 평상시 빌드는 vendor Fil brug_VÆRDI."""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageDraw, ImageFont
To_do_rod = Path(__file__).resolve().parents[1]


def Kør_2():
    sti_Liste = ['/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']
    skrifttype_Liste = [ImageFont.truetype(sti_Liste[0], 13), ImageFont.truetype(sti_Liste[1], 16, index=1), ImageFont.truetype(sti_Liste[2], 16)]
    data = bytearray()
    for tegnkodning in list(range(65536)) + list(range(0x1f600, 0x1f650)):
        tegning_VÆRDI = Image.new('L', (16, 16)); tegne_skærmbillede = ImageDraw.Draw(tegning_VÆRDI)
        if not (tegnkodning < 32 or 0xd800 <= tegnkodning <= 0xdfff):
            tegne_skærmbillede.text((0, -1 if tegnkodning < 256 else -5 if tegnkodning < 65536 else -3), chr(tegnkodning), font=skrifttype_Liste[0 if tegnkodning < 256 else 1 if tegnkodning < 65536 else 2], fill=255)
        for Y_koordinat in range(16):
            BITS_Liste = 0
            for X_koordinat in range(16): BITS_Liste = BITS_Liste * 2 + (tegning_VÆRDI.getpixel((X_koordinat, Y_koordinat)) >= 96)
            data += BITS_Liste.to_bytes(2, 'big')
    mål = To_do_rod / 'vendor/terminal-font.bin'; mål.write_bytes(data)
    이용허락목록 = [Path('/usr/share/doc/fonts-noto-cjk/copyright'), Path('/usr/share/doc/fonts-dejavu-core/copyright')]
    for 원본주소 in 이용허락목록: (To_do_rod / 'vendor' / ('LICENSE.' + 원본주소.parent.name)).write_bytes(원본주소.read_bytes())
    (To_do_rod / 'vendor/terminal-font.json').write_text(json.dumps({'name': 'JKOROS terminal bitmap', 'format': '16 rows, big-endian uint16 mask; BMP then U+1F600..1F64F', 'glyphs': 65536+80, 'sha256': hashlib.sha256(data).hexdigest(), 'sources': {data_placere: hashlib.sha256(Path(data_placere).read_bytes()).hexdigest() for data_placere in sti_Liste}}, indent=2) + '\n')
    print(mål)


if __name__ == '__main__': Kør_2()
