#!/usr/bin/env python3
"""Noto CJK/DejaVu의 라이선스와 출처를 보존한 고정 폭 Terminal 비트맵 ustvariti. 평상시 빌드는 vendor Datoteka uporaba_VALUE."""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageDraw, ImageFont
pobuda_koren = Path(__file__).resolve().parents[1]


def Zaženi():
    pot_Seznam = ['/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']
    pisava_Seznam = [ImageFont.truetype(pot_Seznam[0], 13), ImageFont.truetype(pot_Seznam[1], 16, index=1), ImageFont.truetype(pot_Seznam[2], 16)]
    podatki = bytearray()
    for kodiranje_znakov in list(range(65536)) + list(range(0x1f600, 0x1f650)):
        risba_VALUE = Image.new('L', (16, 16)); 화면그리기 = ImageDraw.Draw(risba_VALUE)
        if not (kodiranje_znakov < 32 or 0xd800 <= kodiranje_znakov <= 0xdfff):
            화면그리기.text((0, -1 if kodiranje_znakov < 256 else -5 if kodiranje_znakov < 65536 else -3), chr(kodiranje_znakov), font=pisava_Seznam[0 if kodiranje_znakov < 256 else 1 if kodiranje_znakov < 65536 else 2], fill=255)
        for 세로좌표 in range(16):
            storitev_Background_Intelligent_Transfer_Service_Seznam = 0
            for koordinata_x in range(16): storitev_Background_Intelligent_Transfer_Service_Seznam = storitev_Background_Intelligent_Transfer_Service_Seznam * 2 + (risba_VALUE.getpixel((koordinata_x, 세로좌표)) >= 96)
            podatki += storitev_Background_Intelligent_Transfer_Service_Seznam.to_bytes(2, 'big')
    tarča = pobuda_koren / 'vendor/terminal-font.bin'; tarča.write_bytes(podatki)
    이용허락목록 = [Path('/usr/share/doc/fonts-noto-cjk/copyright'), Path('/usr/share/doc/fonts-dejavu-core/copyright')]
    for 원본주소 in 이용허락목록: (pobuda_koren / 'vendor' / ('LICENSE.' + 원본주소.parent.name)).write_bytes(원본주소.read_bytes())
    (pobuda_koren / 'vendor/terminal-font.json').write_text(json.dumps({'name': 'JKOROS terminal bitmap', 'format': '16 rows, big-endian uint16 mask; BMP then U+1F600..1F64F', 'glyphs': 65536+80, 'sha256': hashlib.sha256(podatki).hexdigest(), 'sources': {podatki_položaj: hashlib.sha256(Path(podatki_položaj).read_bytes()).hexdigest() for podatki_položaj in pot_Seznam}}, indent=2) + '\n')
    print(tarča)


if __name__ == '__main__': Zaženi()
