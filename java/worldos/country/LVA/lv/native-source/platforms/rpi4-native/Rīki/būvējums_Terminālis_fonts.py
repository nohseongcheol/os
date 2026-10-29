#!/usr/bin/env python3
"""Noto CJK/DejaVu의 라이선스와 출처를 보존한 고정 폭 Terminālis 비트맵 ģenerēt. 평상시 빌드는 vendor Fails lietot_VALUE."""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageDraw, ImageFont
Project_sakne = Path(__file__).resolve().parents[1]


def Palaist():
    ceļš_Saraksts = ['/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']
    fonts_Saraksts = [ImageFont.truetype(ceļš_Saraksts[0], 13), ImageFont.truetype(ceļš_Saraksts[1], 16, index=1), ImageFont.truetype(ceļš_Saraksts[2], 16)]
    dati = bytearray()
    for rakstzīmju_kodēšana in list(range(65536)) + list(range(0x1f600, 0x1f650)):
        zīmējums_VALUE = Image.new('L', (16, 16)); 화면그리기 = ImageDraw.Draw(zīmējums_VALUE)
        if not (rakstzīmju_kodēšana < 32 or 0xd800 <= rakstzīmju_kodēšana <= 0xdfff):
            화면그리기.text((0, -1 if rakstzīmju_kodēšana < 256 else -5 if rakstzīmju_kodēšana < 65536 else -3), chr(rakstzīmju_kodēšana), font=fonts_Saraksts[0 if rakstzīmju_kodēšana < 256 else 1 if rakstzīmju_kodēšana < 65536 else 2], fill=255)
        for 세로좌표 in range(16):
            Background_Intelligent_Transfer_Service_Saraksts = 0
            for x_koordināta in range(16): Background_Intelligent_Transfer_Service_Saraksts = Background_Intelligent_Transfer_Service_Saraksts * 2 + (zīmējums_VALUE.getpixel((x_koordināta, 세로좌표)) >= 96)
            dati += Background_Intelligent_Transfer_Service_Saraksts.to_bytes(2, 'big')
    mērķis = Project_sakne / 'vendor/terminal-font.bin'; mērķis.write_bytes(dati)
    이용허락목록 = [Path('/usr/share/doc/fonts-noto-cjk/copyright'), Path('/usr/share/doc/fonts-dejavu-core/copyright')]
    for 원본주소 in 이용허락목록: (Project_sakne / 'vendor' / ('LICENSE.' + 원본주소.parent.name)).write_bytes(원본주소.read_bytes())
    (Project_sakne / 'vendor/terminal-font.json').write_text(json.dumps({'name': 'JKOROS terminal bitmap', 'format': '16 rows, big-endian uint16 mask; BMP then U+1F600..1F64F', 'glyphs': 65536+80, 'sha256': hashlib.sha256(dati).hexdigest(), 'sources': {dati_amats: hashlib.sha256(Path(dati_amats).read_bytes()).hexdigest() for dati_amats in ceļš_Saraksts}}, indent=2) + '\n')
    print(mērķis)


if __name__ == '__main__': Palaist()
