#!/usr/bin/env python3
"""Noto CJK/DejaVu의 라이선스와 출처를 보존한 고정 폭 টাৰ্মিনেল 비트맵 সৃষ্টি_কৰক. 평상시 빌드는 vendor নথিপত্ৰ 사용."""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageDraw, ImageFont
기준 = Path(__file__).resolve().parents[1]


def সঞ্চালন():
    পথ_সূচী = ['/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']
    ফ_ন্ট_সূচী = [ImageFont.truetype(পথ_সূচী[0], 13), ImageFont.truetype(পথ_সূচী[1], 16, index=1), ImageFont.truetype(পথ_সূচী[2], 16)]
    ডাটা = bytearray()
    for বৰ্ণ_এনকোডিং in list(range(65536)) + list(range(0x1f600, 0x1f650)):
        অংকন_মান = Image.new('L', (16, 16)); 화면그리기 = ImageDraw.Draw(অংকন_মান)
        if not (বৰ্ণ_এনকোডিং < 32 or 0xd800 <= বৰ্ণ_এনকোডিং <= 0xdfff):
            화면그리기.text((0, -1 if বৰ্ণ_এনকোডিং < 256 else -5 if বৰ্ণ_এনকোডিং < 65536 else -3), chr(বৰ্ণ_এনকোডিং), font=ফ_ন্ট_সূচী[0 if বৰ্ণ_এনকোডিং < 256 else 1 if বৰ্ণ_এনকোডিং < 65536 else 2], fill=255)
        for 세로좌표 in range(16):
            비트들 = 0
            for x_ক_ৰ্ডিনেট in range(16): 비트들 = 비트들 * 2 + (অংকন_মান.getpixel((x_ক_ৰ্ডিনেট, 세로좌표)) >= 96)
            ডাটা += 비트들.to_bytes(2, 'big')
    লক্ষ্য = 기준 / 'vendor/terminal-font.bin'; লক্ষ্য.write_bytes(ডাটা)
    이용허락목록 = [Path('/usr/share/doc/fonts-noto-cjk/copyright'), Path('/usr/share/doc/fonts-dejavu-core/copyright')]
    for 원본주소 in 이용허락목록: (기준 / 'vendor' / ('LICENSE.' + 원본주소.parent.name)).write_bytes(원본주소.read_bytes())
    (기준 / 'vendor/terminal-font.json').write_text(json.dumps({'name': 'JKOROS terminal bitmap', 'format': '16 rows, big-endian uint16 mask; BMP then U+1F600..1F64F', 'glyphs': 65536+80, 'sha256': hashlib.sha256(ডাটা).hexdigest(), 'sources': {ডাটা_স্থান_সলনি_কৰক: hashlib.sha256(Path(ডাটা_স্থান_সলনি_কৰক).read_bytes()).hexdigest() for ডাটা_স্থান_সলনি_কৰক in পথ_সূচী}}, indent=2) + '\n')
    print(লক্ষ্য)


if __name__ == '__main__': সঞ্চালন()
