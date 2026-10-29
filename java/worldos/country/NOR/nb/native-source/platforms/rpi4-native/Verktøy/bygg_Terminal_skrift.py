#!/usr/bin/env python3
"""Noto CJK/DejaVu의 라이선스와 출처를 보존한 고정 폭 Terminal 비트맵 generere. 평상시 빌드는 vendor Fil bruk_VERDI."""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageDraw, ImageFont
speile_rot = Path(__file__).resolve().parents[1]


def Kjør_2():
    bane_Liste = ['/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']
    skrift_Liste = [ImageFont.truetype(bane_Liste[0], 13), ImageFont.truetype(bane_Liste[1], 16, index=1), ImageFont.truetype(bane_Liste[2], 16)]
    data = bytearray()
    for tegn_koding in list(range(65536)) + list(range(0x1f600, 0x1f650)):
        tegning_VERDI = Image.new('L', (16, 16)); Tegn_skjermbilde = ImageDraw.Draw(tegning_VERDI)
        if not (tegn_koding < 32 or 0xd800 <= tegn_koding <= 0xdfff):
            Tegn_skjermbilde.text((0, -1 if tegn_koding < 256 else -5 if tegn_koding < 65536 else -3), chr(tegn_koding), font=skrift_Liste[0 if tegn_koding < 256 else 1 if tegn_koding < 65536 else 2], fill=255)
        for Y_koordinat in range(16):
            BITS_Liste = 0
            for x_koordinat in range(16): BITS_Liste = BITS_Liste * 2 + (tegning_VERDI.getpixel((x_koordinat, Y_koordinat)) >= 96)
            data += BITS_Liste.to_bytes(2, 'big')
    mål = speile_rot / 'vendor/terminal-font.bin'; mål.write_bytes(data)
    이용허락목록 = [Path('/usr/share/doc/fonts-noto-cjk/copyright'), Path('/usr/share/doc/fonts-dejavu-core/copyright')]
    for 원본주소 in 이용허락목록: (speile_rot / 'vendor' / ('LICENSE.' + 원본주소.parent.name)).write_bytes(원본주소.read_bytes())
    (speile_rot / 'vendor/terminal-font.json').write_text(json.dumps({'name': 'JKOROS terminal bitmap', 'format': '16 rows, big-endian uint16 mask; BMP then U+1F600..1F64F', 'glyphs': 65536+80, 'sha256': hashlib.sha256(data).hexdigest(), 'sources': {data_plassere: hashlib.sha256(Path(data_plassere).read_bytes()).hexdigest() for data_plassere in bane_Liste}}, indent=2) + '\n')
    print(mål)


if __name__ == '__main__': Kjør_2()
