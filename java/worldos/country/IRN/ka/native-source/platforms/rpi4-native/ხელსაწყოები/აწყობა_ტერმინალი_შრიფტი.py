#!/usr/bin/env python3
"""Noto CJK/DejaVu의 라이선스와 출처를 보존한 고정 폭 ტერმინალი 비트맵 დაგენერირება. 평상시 빌드는 vendor ფაილი 사용."""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageDraw, ImageFont
პროეცირება_ფესვი = Path(__file__).resolve().parents[1]


def გაშვება():
    მდებარეობა_სია = ['/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']
    შრიფტი_სია = [ImageFont.truetype(მდებარეობა_სია[0], 13), ImageFont.truetype(მდებარეობა_სია[1], 16, index=1), ImageFont.truetype(მდებარეობა_სია[2], 16)]
    მონაცემები = bytearray()
    for სიმბოლო_კოდირება in list(range(65536)) + list(range(0x1f600, 0x1f650)):
        ნახატი_მნიშვნელობა_c143fe9e = Image.new('L', (16, 16)); 화면그리기 = ImageDraw.Draw(ნახატი_მნიშვნელობა_c143fe9e)
        if not (სიმბოლო_კოდირება < 32 or 0xd800 <= სიმბოლო_კოდირება <= 0xdfff):
            화면그리기.text((0, -1 if სიმბოლო_კოდირება < 256 else -5 if სიმბოლო_კოდირება < 65536 else -3), chr(სიმბოლო_კოდირება), font=შრიფტი_სია[0 if სიმბოლო_კოდირება < 256 else 1 if სიმბოლო_კოდირება < 65536 else 2], fill=255)
        for Y_ღილაკი_კოორდინატი in range(16):
            비트들 = 0
            for x_კოორდინატა in range(16): 비트들 = 비트들 * 2 + (ნახატი_მნიშვნელობა_c143fe9e.getpixel((x_კოორდინატა, Y_ღილაკი_კოორდინატი)) >= 96)
            მონაცემები += 비트들.to_bytes(2, 'big')
    მიზანი = პროეცირება_ფესვი / 'vendor/terminal-font.bin'; მიზანი.write_bytes(მონაცემები)
    이용허락목록 = [Path('/usr/share/doc/fonts-noto-cjk/copyright'), Path('/usr/share/doc/fonts-dejavu-core/copyright')]
    for 원본주소 in 이용허락목록: (პროეცირება_ფესვი / 'vendor' / ('LICENSE.' + 원본주소.parent.name)).write_bytes(원본주소.read_bytes())
    (პროეცირება_ფესვი / 'vendor/terminal-font.json').write_text(json.dumps({'name': 'JKOROS terminal bitmap', 'format': '16 rows, big-endian uint16 mask; BMP then U+1F600..1F64F', 'glyphs': 65536+80, 'sha256': hashlib.sha256(მონაცემები).hexdigest(), 'sources': {მონაცემები_პოზიცია: hashlib.sha256(Path(მონაცემები_პოზიცია).read_bytes()).hexdigest() for მონაცემები_პოზიცია in მდებარეობა_სია}}, indent=2) + '\n')
    print(მიზანი)


if __name__ == '__main__': გაშვება()
