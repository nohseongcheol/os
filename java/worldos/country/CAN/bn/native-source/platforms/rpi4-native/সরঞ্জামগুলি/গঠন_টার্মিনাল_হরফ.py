#!/usr/bin/env python3
"""Noto CJK/DejaVu의 라이선스와 출처를 보존한 고정 폭 আদেশ_ব্যাখ্যাকারী 비트맵 সৃষ্টি_করুন. 평상시 빌드는 vendor নথির_নাম 사용."""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageDraw, ImageFont
প্রকল্প_মূল = Path(__file__).resolve().parents[1]


def চালনা():
    পথ_তালিকা = ['/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']
    হরফ_তালিকা = [ImageFont.truetype(পথ_তালিকা[0], 13), ImageFont.truetype(পথ_তালিকা[1], 16, index=1), ImageFont.truetype(পথ_তালিকা[2], 16)]
    ডাটা = bytearray()
    for অক্ষর_এনকোড_করা in list(range(65536)) + list(range(0x1f600, 0x1f650)):
        অঙ্কন_মান = Image.new('L', (16, 16)); 화면그리기 = ImageDraw.Draw(অঙ্কন_মান)
        if not (অক্ষর_এনকোড_করা < 32 or 0xd800 <= অক্ষর_এনকোড_করা <= 0xdfff):
            화면그리기.text((0, -1 if অক্ষর_এনকোড_করা < 256 else -5 if অক্ষর_এনকোড_করা < 65536 else -3), chr(অক্ষর_এনকোড_করা), font=হরফ_তালিকা[0 if অক্ষর_এনকোড_করা < 256 else 1 if অক্ষর_এনকোড_করা < 65536 else 2], fill=255)
        for Y_বোতাম_অক্ষবিন্দু in range(16):
            ব্যাকগ্রাউন্ড_ইনটেলিজেন্ট_ট্র্যান্সফার_সার্ভিস_তালিকা = 0
            for X_বোতাম_অক্ষবিন্দু in range(16): ব্যাকগ্রাউন্ড_ইনটেলিজেন্ট_ট্র্যান্সফার_সার্ভিস_তালিকা = ব্যাকগ্রাউন্ড_ইনটেলিজেন্ট_ট্র্যান্সফার_সার্ভিস_তালিকা * 2 + (অঙ্কন_মান.getpixel((X_বোতাম_অক্ষবিন্দু, Y_বোতাম_অক্ষবিন্দু)) >= 96)
            ডাটা += ব্যাকগ্রাউন্ড_ইনটেলিজেন্ট_ট্র্যান্সফার_সার্ভিস_তালিকা.to_bytes(2, 'big')
    লক্ষ্য = প্রকল্প_মূল / 'vendor/terminal-font.bin'; লক্ষ্য.write_bytes(ডাটা)
    이용허락목록 = [Path('/usr/share/doc/fonts-noto-cjk/copyright'), Path('/usr/share/doc/fonts-dejavu-core/copyright')]
    for 원본주소 in 이용허락목록: (প্রকল্প_মূল / 'vendor' / ('LICENSE.' + 원본주소.parent.name)).write_bytes(원본주소.read_bytes())
    (প্রকল্প_মূল / 'vendor/terminal-font.json').write_text(json.dumps({'name': 'JKOROS terminal bitmap', 'format': '16 rows, big-endian uint16 mask; BMP then U+1F600..1F64F', 'glyphs': 65536+80, 'sha256': hashlib.sha256(ডাটা).hexdigest(), 'sources': {ডাটা_পদ: hashlib.sha256(Path(ডাটা_পদ).read_bytes()).hexdigest() for ডাটা_পদ in পথ_তালিকা}}, indent=2) + '\n')
    print(লক্ষ্য)


if __name__ == '__main__': চালনা()
