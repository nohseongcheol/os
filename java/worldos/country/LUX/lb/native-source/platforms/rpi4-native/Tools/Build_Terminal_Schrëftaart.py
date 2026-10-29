#!/usr/bin/env python3
"""Noto CJK/DejaVu의 라이선스와 출처를 보존한 고정 폭 Terminal 비트맵 generéieren. 평상시 빌드는 vendor Fichier 사용."""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageDraw, ImageFont
projezéieren_Racinn = Path(__file__).resolve().parents[1]


def Laf():
    Wee_Lëscht = ['/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']
    Schrëftaart_Lëscht = [ImageFont.truetype(Wee_Lëscht[0], 13), ImageFont.truetype(Wee_Lëscht[1], 16, index=1), ImageFont.truetype(Wee_Lëscht[2], 16)]
    Daten = bytearray()
    for Zeechen_Codéierung in list(range(65536)) + list(range(0x1f600, 0x1f650)):
        Zeechnung_VALUE = Image.new('L', (16, 16)); 화면그리기 = ImageDraw.Draw(Zeechnung_VALUE)
        if not (Zeechen_Codéierung < 32 or 0xd800 <= Zeechen_Codéierung <= 0xdfff):
            화면그리기.text((0, -1 if Zeechen_Codéierung < 256 else -5 if Zeechen_Codéierung < 65536 else -3), chr(Zeechen_Codéierung), font=Schrëftaart_Lëscht[0 if Zeechen_Codéierung < 256 else 1 if Zeechen_Codéierung < 65536 else 2], fill=255)
        for 세로좌표 in range(16):
            비트들 = 0
            for X_Koordinat in range(16): 비트들 = 비트들 * 2 + (Zeechnung_VALUE.getpixel((X_Koordinat, 세로좌표)) >= 96)
            Daten += 비트들.to_bytes(2, 'big')
    Zil = projezéieren_Racinn / 'vendor/terminal-font.bin'; Zil.write_bytes(Daten)
    이용허락목록 = [Path('/usr/share/doc/fonts-noto-cjk/copyright'), Path('/usr/share/doc/fonts-dejavu-core/copyright')]
    for 원본주소 in 이용허락목록: (projezéieren_Racinn / 'vendor' / ('LICENSE.' + 원본주소.parent.name)).write_bytes(원본주소.read_bytes())
    (projezéieren_Racinn / 'vendor/terminal-font.json').write_text(json.dumps({'name': 'JKOROS terminal bitmap', 'format': '16 rows, big-endian uint16 mask; BMP then U+1F600..1F64F', 'glyphs': 65536+80, 'sha256': hashlib.sha256(Daten).hexdigest(), 'sources': {Daten_positionéieren: hashlib.sha256(Path(Daten_positionéieren).read_bytes()).hexdigest() for Daten_positionéieren in Wee_Lëscht}}, indent=2) + '\n')
    print(Zil)


if __name__ == '__main__': Laf()
