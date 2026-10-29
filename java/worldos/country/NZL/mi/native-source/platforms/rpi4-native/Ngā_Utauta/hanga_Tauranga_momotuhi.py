#!/usr/bin/env python3
"""Noto CJK/DejaVu의 라이선스와 출처를 보존한 고정 폭 Tauranga 비트맵 waihanga. 평상시 빌드는 vendor Kōnae 사용."""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageDraw, ImageFont
whakaatu_pūtake = Path(__file__).resolve().parents[1]


def whakahaere():
    ara_Rārangi = ['/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']
    momotuhi_Rārangi = [ImageFont.truetype(ara_Rārangi[0], 13), ImageFont.truetype(ara_Rārangi[1], 16, index=1), ImageFont.truetype(ara_Rārangi[2], 16)]
    raraunga = bytearray()
    for pūāhua_whakawaehere in list(range(65536)) + list(range(0x1f600, 0x1f650)):
        tātuhi_uara = Image.new('L', (16, 16)); 화면그리기 = ImageDraw.Draw(tātuhi_uara)
        if not (pūāhua_whakawaehere < 32 or 0xd800 <= pūāhua_whakawaehere <= 0xdfff):
            화면그리기.text((0, -1 if pūāhua_whakawaehere < 256 else -5 if pūāhua_whakawaehere < 65536 else -3), chr(pūāhua_whakawaehere), font=momotuhi_Rārangi[0 if pūāhua_whakawaehere < 256 else 1 if pūāhua_whakawaehere < 65536 else 2], fill=255)
        for 세로좌표 in range(16):
            비트들 = 0
            for taunga_x in range(16): 비트들 = 비트들 * 2 + (tātuhi_uara.getpixel((taunga_x, 세로좌표)) >= 96)
            raraunga += 비트들.to_bytes(2, 'big')
    ūnga = whakaatu_pūtake / 'vendor/terminal-font.bin'; ūnga.write_bytes(raraunga)
    이용허락목록 = [Path('/usr/share/doc/fonts-noto-cjk/copyright'), Path('/usr/share/doc/fonts-dejavu-core/copyright')]
    for 원본주소 in 이용허락목록: (whakaatu_pūtake / 'vendor' / ('LICENSE.' + 원본주소.parent.name)).write_bytes(원본주소.read_bytes())
    (whakaatu_pūtake / 'vendor/terminal-font.json').write_text(json.dumps({'name': 'JKOROS terminal bitmap', 'format': '16 rows, big-endian uint16 mask; BMP then U+1F600..1F64F', 'glyphs': 65536+80, 'sha256': hashlib.sha256(raraunga).hexdigest(), 'sources': {raraunga_tūranga: hashlib.sha256(Path(raraunga_tūranga).read_bytes()).hexdigest() for raraunga_tūranga in ara_Rārangi}}, indent=2) + '\n')
    print(ūnga)


if __name__ == '__main__': whakahaere()
