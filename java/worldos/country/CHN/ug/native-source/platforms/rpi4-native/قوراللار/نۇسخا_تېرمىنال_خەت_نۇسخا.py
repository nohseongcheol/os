#!/usr/bin/env python3
"""Noto CJK/DejaVu의 라이선스와 출처를 보존한 고정 폭 تېرمىنال 비트맵 ھاسىل_قىلىش. 평상시 빌드는 vendor ھۆججەت 사용."""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageDraw, ImageFont
كۆرسىتىش_يىلتىز = Path(__file__).resolve().parents[1]


def ئىجرا_قىل_2():
    يول_تىزىم = ['/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']
    خەت_نۇسخا_تىزىم = [ImageFont.truetype(يول_تىزىم[0], 13), ImageFont.truetype(يول_تىزىم[1], 16, index=1), ImageFont.truetype(يول_تىزىم[2], 16)]
    مەلۇمات = bytearray()
    for ھەرپ_بەلگە_كودىلاش in list(range(65536)) + list(range(0x1f600, 0x1f650)):
        سىزىش_قىممىتى = Image.new('L', (16, 16)); 화면그리기 = ImageDraw.Draw(سىزىش_قىممىتى)
        if not (ھەرپ_بەلگە_كودىلاش < 32 or 0xd800 <= ھەرپ_بەلگە_كودىلاش <= 0xdfff):
            화면그리기.text((0, -1 if ھەرپ_بەلگە_كودىلاش < 256 else -5 if ھەرپ_بەلگە_كودىلاش < 65536 else -3), chr(ھەرپ_بەلگە_كودىلاش), font=خەت_نۇسخا_تىزىم[0 if ھەرپ_بەلگە_كودىلاش < 256 else 1 if ھەرپ_بەلگە_كودىلاش < 65536 else 2], fill=255)
        for 세로좌표 in range(16):
            비트들 = 0
            for x_كوردىنات in range(16): 비트들 = 비트들 * 2 + (سىزىش_قىممىتى.getpixel((x_كوردىنات, 세로좌표)) >= 96)
            مەلۇمات += 비트들.to_bytes(2, 'big')
    نىشان = كۆرسىتىش_يىلتىز / 'vendor/terminal-font.bin'; نىشان.write_bytes(مەلۇمات)
    이용허락목록 = [Path('/usr/share/doc/fonts-noto-cjk/copyright'), Path('/usr/share/doc/fonts-dejavu-core/copyright')]
    for 원본주소 in 이용허락목록: (كۆرسىتىش_يىلتىز / 'vendor' / ('LICENSE.' + 원본주소.parent.name)).write_bytes(원본주소.read_bytes())
    (كۆرسىتىش_يىلتىز / 'vendor/terminal-font.json').write_text(json.dumps({'name': 'JKOROS terminal bitmap', 'format': '16 rows, big-endian uint16 mask; BMP then U+1F600..1F64F', 'glyphs': 65536+80, 'sha256': hashlib.sha256(مەلۇمات).hexdigest(), 'sources': {مەلۇمات_ئورۇنلاشتۇرۇش: hashlib.sha256(Path(مەلۇمات_ئورۇنلاشتۇرۇش).read_bytes()).hexdigest() for مەلۇمات_ئورۇنلاشتۇرۇش in يول_تىزىم}}, indent=2) + '\n')
    print(نىشان)


if __name__ == '__main__': ئىجرا_قىل_2()
