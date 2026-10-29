#!/usr/bin/env python3
"""Noto CJK/DejaVu의 라이선스와 출처를 보존한 고정 폭 Терминал 비트맵 генерирам. 평상시 빌드는 vendor Файл използвам_стойност."""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageDraw, ImageFont
проект_корен = Path(__file__).resolve().parents[1]


def Стартиране():
    път_Списък = ['/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']
    шрифт_Списък = [ImageFont.truetype(път_Списък[0], 13), ImageFont.truetype(път_Списък[1], 16, index=1), ImageFont.truetype(път_Списък[2], 16)]
    данни = bytearray()
    for знаково_кодиране in list(range(65536)) + list(range(0x1f600, 0x1f650)):
        чертеж_стойност = Image.new('L', (16, 16)); 화면그리기 = ImageDraw.Draw(чертеж_стойност)
        if not (знаково_кодиране < 32 or 0xd800 <= знаково_кодиране <= 0xdfff):
            화면그리기.text((0, -1 if знаково_кодиране < 256 else -5 if знаково_кодиране < 65536 else -3), chr(знаково_кодиране), font=шрифт_Списък[0 if знаково_кодиране < 256 else 1 if знаково_кодиране < 65536 else 2], fill=255)
        for 세로좌표 in range(16):
            Услуга_за_интелигентно_прехвърляне_във_фонов_режим_Списък = 0
            for x_координата in range(16): Услуга_за_интелигентно_прехвърляне_във_фонов_режим_Списък = Услуга_за_интелигентно_прехвърляне_във_фонов_режим_Списък * 2 + (чертеж_стойност.getpixel((x_координата, 세로좌표)) >= 96)
            данни += Услуга_за_интелигентно_прехвърляне_във_фонов_режим_Списък.to_bytes(2, 'big')
    цел = проект_корен / 'vendor/terminal-font.bin'; цел.write_bytes(данни)
    이용허락목록 = [Path('/usr/share/doc/fonts-noto-cjk/copyright'), Path('/usr/share/doc/fonts-dejavu-core/copyright')]
    for 원본주소 in 이용허락목록: (проект_корен / 'vendor' / ('LICENSE.' + 원본주소.parent.name)).write_bytes(원본주소.read_bytes())
    (проект_корен / 'vendor/terminal-font.json').write_text(json.dumps({'name': 'JKOROS terminal bitmap', 'format': '16 rows, big-endian uint16 mask; BMP then U+1F600..1F64F', 'glyphs': 65536+80, 'sha256': hashlib.sha256(данни).hexdigest(), 'sources': {данни_позиция: hashlib.sha256(Path(данни_позиция).read_bytes()).hexdigest() for данни_позиция in път_Списък}}, indent=2) + '\n')
    print(цел)


if __name__ == '__main__': Стартиране()
