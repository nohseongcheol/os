#!/usr/bin/env python3
"""Noto CJK/DejaVu의 라이선스와 출처를 보존한 고정 폭 Терминал 비트맵 генерира. 평상시 빌드는 vendor Датотека 사용."""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageDraw, ImageFont
Project_корен = Path(__file__).resolve().parents[1]


def Изврши_2():
    патека_Список = ['/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']
    фонт_Список = [ImageFont.truetype(патека_Список[0], 13), ImageFont.truetype(патека_Список[1], 16, index=1), ImageFont.truetype(патека_Список[2], 16)]
    податоци = bytearray()
    for знак_кодирање in list(range(65536)) + list(range(0x1f600, 0x1f650)):
        цртеж_VALUE = Image.new('L', (16, 16)); 화면그리기 = ImageDraw.Draw(цртеж_VALUE)
        if not (знак_кодирање < 32 or 0xd800 <= знак_кодирање <= 0xdfff):
            화면그리기.text((0, -1 if знак_кодирање < 256 else -5 if знак_кодирање < 65536 else -3), chr(знак_кодирање), font=фонт_Список[0 if знак_кодирање < 256 else 1 if знак_кодирање < 65536 else 2], fill=255)
        for 세로좌표 in range(16):
            Услуга_за_интелигентен_пренос_во_заднина_Список = 0
            for координата_х in range(16): Услуга_за_интелигентен_пренос_во_заднина_Список = Услуга_за_интелигентен_пренос_во_заднина_Список * 2 + (цртеж_VALUE.getpixel((координата_х, 세로좌표)) >= 96)
            податоци += Услуга_за_интелигентен_пренос_во_заднина_Список.to_bytes(2, 'big')
    цел = Project_корен / 'vendor/terminal-font.bin'; цел.write_bytes(податоци)
    이용허락목록 = [Path('/usr/share/doc/fonts-noto-cjk/copyright'), Path('/usr/share/doc/fonts-dejavu-core/copyright')]
    for 원본주소 in 이용허락목록: (Project_корен / 'vendor' / ('LICENSE.' + 원본주소.parent.name)).write_bytes(원본주소.read_bytes())
    (Project_корен / 'vendor/terminal-font.json').write_text(json.dumps({'name': 'JKOROS terminal bitmap', 'format': '16 rows, big-endian uint16 mask; BMP then U+1F600..1F64F', 'glyphs': 65536+80, 'sha256': hashlib.sha256(податоци).hexdigest(), 'sources': {податоци_позиционирање: hashlib.sha256(Path(податоци_позиционирање).read_bytes()).hexdigest() for податоци_позиционирање in патека_Список}}, indent=2) + '\n')
    print(цел)


if __name__ == '__main__': Изврши_2()
