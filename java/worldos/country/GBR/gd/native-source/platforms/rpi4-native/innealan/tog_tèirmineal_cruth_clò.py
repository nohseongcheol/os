#!/usr/bin/env python3
"""Noto CJK/DejaVu의 라이선스와 출처를 보존한 고정 폭 tèirmineal 비트맵 gin. 평상시 빌드는 vendor faidhle 사용."""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageDraw, ImageFont
tilg_freumh = Path(__file__).resolve().parents[1]


def ruith():
    slighe_Liosta = ['/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']
    cruth_clò_Liosta = [ImageFont.truetype(slighe_Liosta[0], 13), ImageFont.truetype(slighe_Liosta[1], 16, index=1), ImageFont.truetype(slighe_Liosta[2], 16)]
    dàta = bytearray()
    for caractar_còdachadh in list(range(65536)) + list(range(0x1f600, 0x1f650)):
        tarraing_VALUE = Image.new('L', (16, 16)); 화면그리기 = ImageDraw.Draw(tarraing_VALUE)
        if not (caractar_còdachadh < 32 or 0xd800 <= caractar_còdachadh <= 0xdfff):
            화면그리기.text((0, -1 if caractar_còdachadh < 256 else -5 if caractar_còdachadh < 65536 else -3), chr(caractar_còdachadh), font=cruth_clò_Liosta[0 if caractar_còdachadh < 256 else 1 if caractar_còdachadh < 65536 else 2], fill=255)
        for 세로좌표 in range(16):
            비트들 = 0
            for co_chomharra_x in range(16): 비트들 = 비트들 * 2 + (tarraing_VALUE.getpixel((co_chomharra_x, 세로좌표)) >= 96)
            dàta += 비트들.to_bytes(2, 'big')
    targaid = tilg_freumh / 'vendor/terminal-font.bin'; targaid.write_bytes(dàta)
    이용허락목록 = [Path('/usr/share/doc/fonts-noto-cjk/copyright'), Path('/usr/share/doc/fonts-dejavu-core/copyright')]
    for 원본주소 in 이용허락목록: (tilg_freumh / 'vendor' / ('LICENSE.' + 원본주소.parent.name)).write_bytes(원본주소.read_bytes())
    (tilg_freumh / 'vendor/terminal-font.json').write_text(json.dumps({'name': 'JKOROS terminal bitmap', 'format': '16 rows, big-endian uint16 mask; BMP then U+1F600..1F64F', 'glyphs': 65536+80, 'sha256': hashlib.sha256(dàta).hexdigest(), 'sources': {dàta_suidhich: hashlib.sha256(Path(dàta_suidhich).read_bytes()).hexdigest() for dàta_suidhich in slighe_Liosta}}, indent=2) + '\n')
    print(targaid)


if __name__ == '__main__': ruith()
