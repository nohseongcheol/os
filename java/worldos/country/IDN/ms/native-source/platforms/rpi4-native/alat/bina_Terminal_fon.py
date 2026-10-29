#!/usr/bin/env python3
"""Noto CJK/DejaVu의 라이선스와 출처를 보존한 고정 폭 Terminal 비트맵 jana. 평상시 빌드는 vendor Fail 사용."""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageDraw, ImageFont
projek_akar = Path(__file__).resolve().parents[1]


def Jalan():
    laluan_Senarai = ['/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']
    fon_Senarai = [ImageFont.truetype(laluan_Senarai[0], 13), ImageFont.truetype(laluan_Senarai[1], 16, index=1), ImageFont.truetype(laluan_Senarai[2], 16)]
    data = bytearray()
    for pengekodan_aksara in list(range(65536)) + list(range(0x1f600, 0x1f650)):
        lukisan_VALUE = Image.new('L', (16, 16)); 화면그리기 = ImageDraw.Draw(lukisan_VALUE)
        if not (pengekodan_aksara < 32 or 0xd800 <= pengekodan_aksara <= 0xdfff):
            화면그리기.text((0, -1 if pengekodan_aksara < 256 else -5 if pengekodan_aksara < 65536 else -3), chr(pengekodan_aksara), font=fon_Senarai[0 if pengekodan_aksara < 256 else 1 if pengekodan_aksara < 65536 else 2], fill=255)
        for Y_koordinat in range(16):
            Background_Intelligent_Transfer_Service_Senarai = 0
            for koordinat_x in range(16): Background_Intelligent_Transfer_Service_Senarai = Background_Intelligent_Transfer_Service_Senarai * 2 + (lukisan_VALUE.getpixel((koordinat_x, Y_koordinat)) >= 96)
            data += Background_Intelligent_Transfer_Service_Senarai.to_bytes(2, 'big')
    sasaran = projek_akar / 'vendor/terminal-font.bin'; sasaran.write_bytes(data)
    이용허락목록 = [Path('/usr/share/doc/fonts-noto-cjk/copyright'), Path('/usr/share/doc/fonts-dejavu-core/copyright')]
    for 원본주소 in 이용허락목록: (projek_akar / 'vendor' / ('LICENSE.' + 원본주소.parent.name)).write_bytes(원본주소.read_bytes())
    (projek_akar / 'vendor/terminal-font.json').write_text(json.dumps({'name': 'JKOROS terminal bitmap', 'format': '16 rows, big-endian uint16 mask; BMP then U+1F600..1F64F', 'glyphs': 65536+80, 'sha256': hashlib.sha256(data).hexdigest(), 'sources': {data_jawatan: hashlib.sha256(Path(data_jawatan).read_bytes()).hexdigest() for data_jawatan in laluan_Senarai}}, indent=2) + '\n')
    print(sasaran)


if __name__ == '__main__': Jalan()
