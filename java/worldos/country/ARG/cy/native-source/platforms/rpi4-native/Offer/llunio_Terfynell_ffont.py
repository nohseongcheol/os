#!/usr/bin/env python3
"""Noto CJK/DejaVu의 라이선스와 출처를 보존한 고정 폭 Terfynell 비트맵 cynhyrchu. 평상시 빌드는 vendor Ffeil 사용."""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageDraw, ImageFont
prosiect_gwraidd = Path(__file__).resolve().parents[1]


def Gweithredu_2():
    llwybr_Rhestr = ['/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']
    ffont_Rhestr = [ImageFont.truetype(llwybr_Rhestr[0], 13), ImageFont.truetype(llwybr_Rhestr[1], 16, index=1), ImageFont.truetype(llwybr_Rhestr[2], 16)]
    data = bytearray()
    for nod_amgodio in list(range(65536)) + list(range(0x1f600, 0x1f650)):
        lluniad_VALUE = Image.new('L', (16, 16)); 화면그리기 = ImageDraw.Draw(lluniad_VALUE)
        if not (nod_amgodio < 32 or 0xd800 <= nod_amgodio <= 0xdfff):
            화면그리기.text((0, -1 if nod_amgodio < 256 else -5 if nod_amgodio < 65536 else -3), chr(nod_amgodio), font=ffont_Rhestr[0 if nod_amgodio < 256 else 1 if nod_amgodio < 65536 else 2], fill=255)
        for Y_cyfesuryn in range(16):
            비트들 = 0
            for cyfesuryn_x in range(16): 비트들 = 비트들 * 2 + (lluniad_VALUE.getpixel((cyfesuryn_x, Y_cyfesuryn)) >= 96)
            data += 비트들.to_bytes(2, 'big')
    targed = prosiect_gwraidd / 'vendor/terminal-font.bin'; targed.write_bytes(data)
    이용허락목록 = [Path('/usr/share/doc/fonts-noto-cjk/copyright'), Path('/usr/share/doc/fonts-dejavu-core/copyright')]
    for 원본주소 in 이용허락목록: (prosiect_gwraidd / 'vendor' / ('LICENSE.' + 원본주소.parent.name)).write_bytes(원본주소.read_bytes())
    (prosiect_gwraidd / 'vendor/terminal-font.json').write_text(json.dumps({'name': 'JKOROS terminal bitmap', 'format': '16 rows, big-endian uint16 mask; BMP then U+1F600..1F64F', 'glyphs': 65536+80, 'sha256': hashlib.sha256(data).hexdigest(), 'sources': {data_safle: hashlib.sha256(Path(data_safle).read_bytes()).hexdigest() for data_safle in llwybr_Rhestr}}, indent=2) + '\n')
    print(targed)


if __name__ == '__main__': Gweithredu_2()
