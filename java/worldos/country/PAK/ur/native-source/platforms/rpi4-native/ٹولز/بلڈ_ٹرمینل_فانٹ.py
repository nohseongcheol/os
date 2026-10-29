#!/usr/bin/env python3
"""Noto CJK/DejaVu의 라이선스와 출처를 보존한 고정 폭 حکم_کی_تشریح_کرنے_والا 비트맵 تخلیق_کرنا. 평상시 빌드는 vendor فائل_کا_نام 사용."""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageDraw, ImageFont
عکس_ڈالنا_روٹ = Path(__file__).resolve().parents[1]


def چلائیں():
    راہ_فہرست = ['/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']
    فانٹ_فہرست = [ImageFont.truetype(راہ_فہرست[0], 13), ImageFont.truetype(راہ_فہرست[1], 16, index=1), ImageFont.truetype(راہ_فہرست[2], 16)]
    کوائف = bytearray()
    for کریکٹر_ضابطہ_بندی in list(range(65536)) + list(range(0x1f600, 0x1f650)):
        ڈرائنگ_قدر = Image.new('L', (16, 16)); 화면그리기 = ImageDraw.Draw(ڈرائنگ_قدر)
        if not (کریکٹر_ضابطہ_بندی < 32 or 0xd800 <= کریکٹر_ضابطہ_بندی <= 0xdfff):
            화면그리기.text((0, -1 if کریکٹر_ضابطہ_بندی < 256 else -5 if کریکٹر_ضابطہ_بندی < 65536 else -3), chr(کریکٹر_ضابطہ_بندی), font=فانٹ_فہرست[0 if کریکٹر_ضابطہ_بندی < 256 else 1 if کریکٹر_ضابطہ_بندی < 65536 else 2], fill=255)
        for 세로좌표 in range(16):
            비트들 = 0
            for ایکس_مربوط in range(16): 비트들 = 비트들 * 2 + (ڈرائنگ_قدر.getpixel((ایکس_مربوط, 세로좌표)) >= 96)
            کوائف += 비트들.to_bytes(2, 'big')
    ہدف = عکس_ڈالنا_روٹ / 'vendor/terminal-font.bin'; ہدف.write_bytes(کوائف)
    이용허락목록 = [Path('/usr/share/doc/fonts-noto-cjk/copyright'), Path('/usr/share/doc/fonts-dejavu-core/copyright')]
    for 원본주소 in 이용허락목록: (عکس_ڈالنا_روٹ / 'vendor' / ('LICENSE.' + 원본주소.parent.name)).write_bytes(원본주소.read_bytes())
    (عکس_ڈالنا_روٹ / 'vendor/terminal-font.json').write_text(json.dumps({'name': 'JKOROS terminal bitmap', 'format': '16 rows, big-endian uint16 mask; BMP then U+1F600..1F64F', 'glyphs': 65536+80, 'sha256': hashlib.sha256(کوائف).hexdigest(), 'sources': {کوائف_پوزیشن_ٹھیک_کریں: hashlib.sha256(Path(کوائف_پوزیشن_ٹھیک_کریں).read_bytes()).hexdigest() for کوائف_پوزیشن_ٹھیک_کریں in راہ_فہرست}}, indent=2) + '\n')
    print(ہدف)


if __name__ == '__main__': چلائیں()
