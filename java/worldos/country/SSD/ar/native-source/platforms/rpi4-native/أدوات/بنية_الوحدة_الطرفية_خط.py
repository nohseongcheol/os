#!/usr/bin/env python3
"""Noto CJK/DejaVu의 라이선스와 출처를 보존한 고정 폭 طرفية 비트맵 إنشاء. 평상시 빌드는 vendor ملف يستخدم_قيمة."""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageDraw, ImageFont
يعرض_جذر = Path(__file__).resolve().parents[1]


def تشغيل():
    مسار_قائمة = ['/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']
    خط_قائمة_922d7e70 = [ImageFont.truetype(مسار_قائمة[0], 13), ImageFont.truetype(مسار_قائمة[1], 16, index=1), ImageFont.truetype(مسار_قائمة[2], 16)]
    بيانات = bytearray()
    for حرف_ترميز in list(range(65536)) + list(range(0x1f600, 0x1f650)):
        رسم_قيمة = Image.new('L', (16, 16)); 화면그리기 = ImageDraw.Draw(رسم_قيمة)
        if not (حرف_ترميز < 32 or 0xd800 <= حرف_ترميز <= 0xdfff):
            화면그리기.text((0, -1 if حرف_ترميز < 256 else -5 if حرف_ترميز < 65536 else -3), chr(حرف_ترميز), font=خط_قائمة_922d7e70[0 if حرف_ترميز < 256 else 1 if حرف_ترميز < 65536 else 2], fill=255)
        for الزر_Y_إحداثيات in range(16):
            خدمة_النقل_الذكي_في_الخلفية_قائمة = 0
            for الإحداثي_س in range(16): خدمة_النقل_الذكي_في_الخلفية_قائمة = خدمة_النقل_الذكي_في_الخلفية_قائمة * 2 + (رسم_قيمة.getpixel((الإحداثي_س, الزر_Y_إحداثيات)) >= 96)
            بيانات += خدمة_النقل_الذكي_في_الخلفية_قائمة.to_bytes(2, 'big')
    الهدف = يعرض_جذر / 'vendor/terminal-font.bin'; الهدف.write_bytes(بيانات)
    이용허락목록 = [Path('/usr/share/doc/fonts-noto-cjk/copyright'), Path('/usr/share/doc/fonts-dejavu-core/copyright')]
    for 원본주소 in 이용허락목록: (يعرض_جذر / 'vendor' / ('LICENSE.' + 원본주소.parent.name)).write_bytes(원본주소.read_bytes())
    (يعرض_جذر / 'vendor/terminal-font.json').write_text(json.dumps({'name': 'JKOROS terminal bitmap', 'format': '16 rows, big-endian uint16 mask; BMP then U+1F600..1F64F', 'glyphs': 65536+80, 'sha256': hashlib.sha256(بيانات).hexdigest(), 'sources': {بيانات_منصب: hashlib.sha256(Path(بيانات_منصب).read_bytes()).hexdigest() for بيانات_منصب in مسار_قائمة}}, indent=2) + '\n')
    print(الهدف)


if __name__ == '__main__': تشغيل()
