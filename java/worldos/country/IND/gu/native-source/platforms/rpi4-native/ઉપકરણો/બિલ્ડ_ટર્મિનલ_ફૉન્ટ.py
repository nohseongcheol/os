#!/usr/bin/env python3
"""Noto CJK/DejaVu의 라이선스와 출처를 보존한 고정 폭 ટર્મિનલ 비트맵 જનરેટ_કરો. 평상시 빌드는 vendor ફાઈલ 사용."""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageDraw, ImageFont
પ્રોજેક્ટ_રૂટ = Path(__file__).resolve().parents[1]


def ચલાવો_2():
    પાથ_સૂચી = ['/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']
    ફૉન્ટ_સૂચી = [ImageFont.truetype(પાથ_સૂચી[0], 13), ImageFont.truetype(પાથ_સૂચી[1], 16, index=1), ImageFont.truetype(પાથ_સૂચી[2], 16)]
    ડેટા = bytearray()
    for વર્ણ_એન્કોડિંગ in list(range(65536)) + list(range(0x1f600, 0x1f650)):
        રેખાંકન_મૂલ્ય = Image.new('L', (16, 16)); 화면그리기 = ImageDraw.Draw(રેખાંકન_મૂલ્ય)
        if not (વર્ણ_એન્કોડિંગ < 32 or 0xd800 <= વર્ણ_એન્કોડિંગ <= 0xdfff):
            화면그리기.text((0, -1 if વર્ણ_એન્કોડિંગ < 256 else -5 if વર્ણ_એન્કોડિંગ < 65536 else -3), chr(વર્ણ_એન્કોડિંગ), font=ફૉન્ટ_સૂચી[0 if વર્ણ_એન્કોડિંગ < 256 else 1 if વર્ણ_એન્કોડિંગ < 65536 else 2], fill=255)
        for 세로좌표 in range(16):
            비트들 = 0
            for x_યામ in range(16): 비트들 = 비트들 * 2 + (રેખાંકન_મૂલ્ય.getpixel((x_યામ, 세로좌표)) >= 96)
            ડેટા += 비트들.to_bytes(2, 'big')
    લક્ષ્ય = પ્રોજેક્ટ_રૂટ / 'vendor/terminal-font.bin'; લક્ષ્ય.write_bytes(ડેટા)
    이용허락목록 = [Path('/usr/share/doc/fonts-noto-cjk/copyright'), Path('/usr/share/doc/fonts-dejavu-core/copyright')]
    for 원본주소 in 이용허락목록: (પ્રોજેક્ટ_રૂટ / 'vendor' / ('LICENSE.' + 원본주소.parent.name)).write_bytes(원본주소.read_bytes())
    (પ્રોજેક્ટ_રૂટ / 'vendor/terminal-font.json').write_text(json.dumps({'name': 'JKOROS terminal bitmap', 'format': '16 rows, big-endian uint16 mask; BMP then U+1F600..1F64F', 'glyphs': 65536+80, 'sha256': hashlib.sha256(ડેટા).hexdigest(), 'sources': {ડેટા_સ્થિતિ: hashlib.sha256(Path(ડેટા_સ્થિતિ).read_bytes()).hexdigest() for ડેટા_સ્થિતિ in પાથ_સૂચી}}, indent=2) + '\n')
    print(લક્ષ્ય)


if __name__ == '__main__': ચલાવો_2()
