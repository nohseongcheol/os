#!/usr/bin/env python3
"""Noto CJK/DejaVu의 라이선스와 출처를 보존한 고정 폭 терминал 비트맵 генерировать. 평상시 빌드는 vendor файл использовать_ЗНАЧЕН."""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageDraw, ImageFont
задача_корень = Path(__file__).resolve().parents[1]


def запустить():
    путь_Список = ['/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']
    шрифт_Список = [ImageFont.truetype(путь_Список[0], 13), ImageFont.truetype(путь_Список[1], 16, index=1), ImageFont.truetype(путь_Список[2], 16)]
    данные = bytearray()
    for кодировка_символов in list(range(65536)) + list(range(0x1f600, 0x1f650)):
        рисунок_ЗНАЧЕН = Image.new('L', (16, 16)); выписать_экран = ImageDraw.Draw(рисунок_ЗНАЧЕН)
        if not (кодировка_символов < 32 or 0xd800 <= кодировка_символов <= 0xdfff):
            выписать_экран.text((0, -1 if кодировка_символов < 256 else -5 if кодировка_символов < 65536 else -3), chr(кодировка_символов), font=шрифт_Список[0 if кодировка_символов < 256 else 1 if кодировка_символов < 65536 else 2], fill=255)
        for Y_координата in range(16):
            BITS_Список = 0
            for координата_X in range(16): BITS_Список = BITS_Список * 2 + (рисунок_ЗНАЧЕН.getpixel((координата_X, Y_координата)) >= 96)
            данные += BITS_Список.to_bytes(2, 'big')
    целевое_значение = задача_корень / 'vendor/terminal-font.bin'; целевое_значение.write_bytes(данные)
    이용허락목록 = [Path('/usr/share/doc/fonts-noto-cjk/copyright'), Path('/usr/share/doc/fonts-dejavu-core/copyright')]
    for 원본주소 in 이용허락목록: (задача_корень / 'vendor' / ('LICENSE.' + 원본주소.parent.name)).write_bytes(원본주소.read_bytes())
    (задача_корень / 'vendor/terminal-font.json').write_text(json.dumps({'name': 'JKOROS terminal bitmap', 'format': '16 rows, big-endian uint16 mask; BMP then U+1F600..1F64F', 'glyphs': 65536+80, 'sha256': hashlib.sha256(данные).hexdigest(), 'sources': {данные_позиция: hashlib.sha256(Path(данные_позиция).read_bytes()).hexdigest() for данные_позиция in путь_Список}}, indent=2) + '\n')
    print(целевое_значение)


if __name__ == '__main__': запустить()
