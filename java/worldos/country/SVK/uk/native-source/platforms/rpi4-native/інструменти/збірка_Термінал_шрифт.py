#!/usr/bin/env python3
"""Noto CJK/DejaVu의 라이선스와 출처를 보존한 고정 폭 термінал 비트맵 генерувати. 평상시 빌드는 vendor файл використання_значення."""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageDraw, ImageFont
Дії_корінь = Path(__file__).resolve().parents[1]


def запустити():
    шлях_список = ['/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']
    шрифт_список = [ImageFont.truetype(шлях_список[0], 13), ImageFont.truetype(шлях_список[1], 16, index=1), ImageFont.truetype(шлях_список[2], 16)]
    дані = bytearray()
    for кодування_символів in list(range(65536)) + list(range(0x1f600, 0x1f650)):
        малювання_значення = Image.new('L', (16, 16)); 화면그리기 = ImageDraw.Draw(малювання_значення)
        if not (кодування_символів < 32 or 0xd800 <= кодування_символів <= 0xdfff):
            화면그리기.text((0, -1 if кодування_символів < 256 else -5 if кодування_символів < 65536 else -3), chr(кодування_символів), font=шрифт_список[0 if кодування_символів < 256 else 1 if кодування_символів < 65536 else 2], fill=255)
        for 세로좌표 in range(16):
            служба_фонового_передавання_файлів_список = 0
            for координата_X in range(16): служба_фонового_передавання_файлів_список = служба_фонового_передавання_файлів_список * 2 + (малювання_значення.getpixel((координата_X, 세로좌표)) >= 96)
            дані += служба_фонового_передавання_файлів_список.to_bytes(2, 'big')
    мета = Дії_корінь / 'vendor/terminal-font.bin'; мета.write_bytes(дані)
    이용허락목록 = [Path('/usr/share/doc/fonts-noto-cjk/copyright'), Path('/usr/share/doc/fonts-dejavu-core/copyright')]
    for 원본주소 in 이용허락목록: (Дії_корінь / 'vendor' / ('LICENSE.' + 원본주소.parent.name)).write_bytes(원본주소.read_bytes())
    (Дії_корінь / 'vendor/terminal-font.json').write_text(json.dumps({'name': 'JKOROS terminal bitmap', 'format': '16 rows, big-endian uint16 mask; BMP then U+1F600..1F64F', 'glyphs': 65536+80, 'sha256': hashlib.sha256(дані).hexdigest(), 'sources': {дані_посада: hashlib.sha256(Path(дані_посада).read_bytes()).hexdigest() for дані_посада in шлях_список}}, indent=2) + '\n')
    print(мета)


if __name__ == '__main__': запустити()
