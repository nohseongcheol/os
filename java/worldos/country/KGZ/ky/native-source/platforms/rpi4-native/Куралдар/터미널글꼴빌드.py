#!/usr/bin/env python3
"""Noto CJK/DejaVu의 라이선스와 출처를 보존한 고정 폭 Терминал 비트맵 생성. 평상시 빌드는 vendor Файл 사용."""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageDraw, ImageFont
기준 = Path(__file__).resolve().parents[1]


def Жүргүзүү():
    жол_Тизме = ['/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']
    арип_Тизме = [ImageFont.truetype(жол_Тизме[0], 13), ImageFont.truetype(жол_Тизме[1], 16, index=1), ImageFont.truetype(жол_Тизме[2], 16)]
    берилмелер = bytearray()
    for символ_коддоо in list(range(65536)) + list(range(0x1f600, 0x1f650)):
        чийүү_маани = Image.new('L', (16, 16)); 화면그리기 = ImageDraw.Draw(чийүү_маани)
        if not (символ_коддоо < 32 or 0xd800 <= символ_коддоо <= 0xdfff):
            화면그리기.text((0, -1 if символ_коддоо < 256 else -5 if символ_коддоо < 65536 else -3), chr(символ_коддоо), font=арип_Тизме[0 if символ_коддоо < 256 else 1 if символ_коддоо < 65536 else 2], fill=255)
        for 세로좌표 in range(16):
            비트들 = 0
            for x_координата in range(16): 비트들 = 비트들 * 2 + (чийүү_маани.getpixel((x_координата, 세로좌표)) >= 96)
            берилмелер += 비트들.to_bytes(2, 'big')
    максат = 기준 / 'vendor/terminal-font.bin'; максат.write_bytes(берилмелер)
    이용허락목록 = [Path('/usr/share/doc/fonts-noto-cjk/copyright'), Path('/usr/share/doc/fonts-dejavu-core/copyright')]
    for 원본주소 in 이용허락목록: (기준 / 'vendor' / ('LICENSE.' + 원본주소.parent.name)).write_bytes(원본주소.read_bytes())
    (기준 / 'vendor/terminal-font.json').write_text(json.dumps({'name': 'JKOROS terminal bitmap', 'format': '16 rows, big-endian uint16 mask; BMP then U+1F600..1F64F', 'glyphs': 65536+80, 'sha256': hashlib.sha256(берилмелер).hexdigest(), 'sources': {자료위치: hashlib.sha256(Path(자료위치).read_bytes()).hexdigest() for 자료위치 in жол_Тизме}}, indent=2) + '\n')
    print(максат)


if __name__ == '__main__': Жүргүзүү()
