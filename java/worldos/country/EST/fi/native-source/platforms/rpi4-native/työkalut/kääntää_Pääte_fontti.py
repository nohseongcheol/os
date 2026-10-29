#!/usr/bin/env python3
"""Noto CJK/DejaVu의 라이선스와 출처를 보존한 고정 폭 komentotulkki 비트맵 generoida. 평상시 빌드는 vendor tiedoston_nimi käyttö_ARVO."""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageDraw, ImageFont
aloite_juuri = Path(__file__).resolve().parents[1]


def Suorita_2():
    polku_luettelo = ['/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']
    fontti_luettelo = [ImageFont.truetype(polku_luettelo[0], 13), ImageFont.truetype(polku_luettelo[1], 16, index=1), ImageFont.truetype(polku_luettelo[2], 16)]
    data = bytearray()
    for merkkikoodaus in list(range(65536)) + list(range(0x1f600, 0x1f650)):
        piirustus_ARVO = Image.new('L', (16, 16)); 화면그리기 = ImageDraw.Draw(piirustus_ARVO)
        if not (merkkikoodaus < 32 or 0xd800 <= merkkikoodaus <= 0xdfff):
            화면그리기.text((0, -1 if merkkikoodaus < 256 else -5 if merkkikoodaus < 65536 else -3), chr(merkkikoodaus), font=fontti_luettelo[0 if merkkikoodaus < 256 else 1 if merkkikoodaus < 65536 else 2], fill=255)
        for Y_koordinaatti in range(16):
            Background_Intelligent_Transfer_Service_luettelo = 0
            for x_koordinaatti in range(16): Background_Intelligent_Transfer_Service_luettelo = Background_Intelligent_Transfer_Service_luettelo * 2 + (piirustus_ARVO.getpixel((x_koordinaatti, Y_koordinaatti)) >= 96)
            data += Background_Intelligent_Transfer_Service_luettelo.to_bytes(2, 'big')
    tavoite = aloite_juuri / 'vendor/terminal-font.bin'; tavoite.write_bytes(data)
    이용허락목록 = [Path('/usr/share/doc/fonts-noto-cjk/copyright'), Path('/usr/share/doc/fonts-dejavu-core/copyright')]
    for 원본주소 in 이용허락목록: (aloite_juuri / 'vendor' / ('LICENSE.' + 원본주소.parent.name)).write_bytes(원본주소.read_bytes())
    (aloite_juuri / 'vendor/terminal-font.json').write_text(json.dumps({'name': 'JKOROS terminal bitmap', 'format': '16 rows, big-endian uint16 mask; BMP then U+1F600..1F64F', 'glyphs': 65536+80, 'sha256': hashlib.sha256(data).hexdigest(), 'sources': {data_toimi: hashlib.sha256(Path(data_toimi).read_bytes()).hexdigest() for data_toimi in polku_luettelo}}, indent=2) + '\n')
    print(tavoite)


if __name__ == '__main__': Suorita_2()
