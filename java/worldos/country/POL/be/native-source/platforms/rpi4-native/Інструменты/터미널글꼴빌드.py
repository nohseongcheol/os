#!/usr/bin/env python3
"""Noto CJK/DejaVu의 라이선스와 출처를 보존한 고정 폭 Тэрмінал 비트맵 생성. 평상시 빌드는 vendor Файл 사용."""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageDraw, ImageFont
기준 = Path(__file__).resolve().parents[1]


def Выканаць():
    шлях_Спіс = ['/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']
    шрыфт_Спіс = [ImageFont.truetype(шлях_Спіс[0], 13), ImageFont.truetype(шлях_Спіс[1], 16, index=1), ImageFont.truetype(шлях_Спіс[2], 16)]
    дадзеныя = bytearray()
    for сімвал_кадаванне in list(range(65536)) + list(range(0x1f600, 0x1f650)):
        рукапісная_графіка_значэнне = Image.new('L', (16, 16)); 화면그리기 = ImageDraw.Draw(рукапісная_графіка_значэнне)
        if not (сімвал_кадаванне < 32 or 0xd800 <= сімвал_кадаванне <= 0xdfff):
            화면그리기.text((0, -1 if сімвал_кадаванне < 256 else -5 if сімвал_кадаванне < 65536 else -3), chr(сімвал_кадаванне), font=шрыфт_Спіс[0 if сімвал_кадаванне < 256 else 1 if сімвал_кадаванне < 65536 else 2], fill=255)
        for 세로좌표 in range(16):
            Служба_інтэлектуальнай_фонавай_перадачы_файлаў_Спіс = 0
            for каардыната_x in range(16): Служба_інтэлектуальнай_фонавай_перадачы_файлаў_Спіс = Служба_інтэлектуальнай_фонавай_перадачы_файлаў_Спіс * 2 + (рукапісная_графіка_значэнне.getpixel((каардыната_x, 세로좌표)) >= 96)
            дадзеныя += Служба_інтэлектуальнай_фонавай_перадачы_файлаў_Спіс.to_bytes(2, 'big')
    мэтавы_паказчык = 기준 / 'vendor/terminal-font.bin'; мэтавы_паказчык.write_bytes(дадзеныя)
    이용허락목록 = [Path('/usr/share/doc/fonts-noto-cjk/copyright'), Path('/usr/share/doc/fonts-dejavu-core/copyright')]
    for 원본주소 in 이용허락목록: (기준 / 'vendor' / ('LICENSE.' + 원본주소.parent.name)).write_bytes(원본주소.read_bytes())
    (기준 / 'vendor/terminal-font.json').write_text(json.dumps({'name': 'JKOROS terminal bitmap', 'format': '16 rows, big-endian uint16 mask; BMP then U+1F600..1F64F', 'glyphs': 65536+80, 'sha256': hashlib.sha256(дадзеныя).hexdigest(), 'sources': {자료위치: hashlib.sha256(Path(자료위치).read_bytes()).hexdigest() for 자료위치 in шлях_Спіс}}, indent=2) + '\n')
    print(мэтавы_паказчык)


if __name__ == '__main__': Выканаць()
