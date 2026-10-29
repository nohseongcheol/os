#!/usr/bin/env python3
"""Noto CJK/DejaVu의 라이선스와 출처를 보존한 고정 폭 Терминал 비트맵 генерисати. 평상시 빌드는 vendor Датотека 사용."""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageDraw, ImageFont
пројектовати_корен = Path(__file__).resolve().parents[1]


def Покрени():
    пут_Листа = ['/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']
    фонт_Листа = [ImageFont.truetype(пут_Листа[0], 13), ImageFont.truetype(пут_Листа[1], 16, index=1), ImageFont.truetype(пут_Листа[2], 16)]
    подаци = bytearray()
    for знак_кодирање in list(range(65536)) + list(range(0x1f600, 0x1f650)):
        цртеж_вриједност = Image.new('L', (16, 16)); 화면그리기 = ImageDraw.Draw(цртеж_вриједност)
        if not (знак_кодирање < 32 or 0xd800 <= знак_кодирање <= 0xdfff):
            화면그리기.text((0, -1 if знак_кодирање < 256 else -5 if знак_кодирање < 65536 else -3), chr(знак_кодирање), font=фонт_Листа[0 if знак_кодирање < 256 else 1 if знак_кодирање < 65536 else 2], fill=255)
        for дугме_Y_координата in range(16):
            Услуга_интелигентног_преноса_у_позадини_Листа = 0
            for x_координата in range(16): Услуга_интелигентног_преноса_у_позадини_Листа = Услуга_интелигентног_преноса_у_позадини_Листа * 2 + (цртеж_вриједност.getpixel((x_координата, дугме_Y_координата)) >= 96)
            подаци += Услуга_интелигентног_преноса_у_позадини_Листа.to_bytes(2, 'big')
    циљ = пројектовати_корен / 'vendor/terminal-font.bin'; циљ.write_bytes(подаци)
    이용허락목록 = [Path('/usr/share/doc/fonts-noto-cjk/copyright'), Path('/usr/share/doc/fonts-dejavu-core/copyright')]
    for 원본주소 in 이용허락목록: (пројектовати_корен / 'vendor' / ('LICENSE.' + 원본주소.parent.name)).write_bytes(원본주소.read_bytes())
    (пројектовати_корен / 'vendor/terminal-font.json').write_text(json.dumps({'name': 'JKOROS terminal bitmap', 'format': '16 rows, big-endian uint16 mask; BMP then U+1F600..1F64F', 'glyphs': 65536+80, 'sha256': hashlib.sha256(подаци).hexdigest(), 'sources': {подаци_позиција: hashlib.sha256(Path(подаци_позиција).read_bytes()).hexdigest() for подаци_позиција in пут_Листа}}, indent=2) + '\n')
    print(циљ)


if __name__ == '__main__': Покрени()
