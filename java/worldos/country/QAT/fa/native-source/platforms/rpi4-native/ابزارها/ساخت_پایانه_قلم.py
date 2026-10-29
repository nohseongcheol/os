#!/usr/bin/env python3
"""Noto CJK/DejaVu의 라이선스와 출처를 보존한 고정 폭 پایانه 비트맵 ایجاد. 평상시 빌드는 vendor پرونده 사용."""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageDraw, ImageFont
نمایش_دادن_جذر = Path(__file__).resolve().parents[1]


def اجرا_2():
    مسیر_لیست = ['/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']
    قلم_لیست = [ImageFont.truetype(مسیر_لیست[0], 13), ImageFont.truetype(مسیر_لیست[1], 16, index=1), ImageFont.truetype(مسیر_لیست[2], 16)]
    داده_ها = bytearray()
    for نویسه_رمزگذاری in list(range(65536)) + list(range(0x1f600, 0x1f650)):
        نقاشی_مقدار = Image.new('L', (16, 16)); 화면그리기 = ImageDraw.Draw(نقاشی_مقدار)
        if not (نویسه_رمزگذاری < 32 or 0xd800 <= نویسه_رمزگذاری <= 0xdfff):
            화면그리기.text((0, -1 if نویسه_رمزگذاری < 256 else -5 if نویسه_رمزگذاری < 65536 else -3), chr(نویسه_رمزگذاری), font=قلم_لیست[0 if نویسه_رمزگذاری < 256 else 1 if نویسه_رمزگذاری < 65536 else 2], fill=255)
        for دکمه_Y_مختصات in range(16):
            비트들 = 0
            for مختصات_x in range(16): 비트들 = 비트들 * 2 + (نقاشی_مقدار.getpixel((مختصات_x, دکمه_Y_مختصات)) >= 96)
            داده_ها += 비트들.to_bytes(2, 'big')
    هدف = نمایش_دادن_جذر / 'vendor/terminal-font.bin'; هدف.write_bytes(داده_ها)
    이용허락목록 = [Path('/usr/share/doc/fonts-noto-cjk/copyright'), Path('/usr/share/doc/fonts-dejavu-core/copyright')]
    for 원본주소 in 이용허락목록: (نمایش_دادن_جذر / 'vendor' / ('LICENSE.' + 원본주소.parent.name)).write_bytes(원본주소.read_bytes())
    (نمایش_دادن_جذر / 'vendor/terminal-font.json').write_text(json.dumps({'name': 'JKOROS terminal bitmap', 'format': '16 rows, big-endian uint16 mask; BMP then U+1F600..1F64F', 'glyphs': 65536+80, 'sha256': hashlib.sha256(داده_ها).hexdigest(), 'sources': {داده_ها_مرتب_کردن: hashlib.sha256(Path(داده_ها_مرتب_کردن).read_bytes()).hexdigest() for داده_ها_مرتب_کردن in مسیر_لیست}}, indent=2) + '\n')
    print(هدف)


if __name__ == '__main__': اجرا_2()
