#!/usr/bin/env python3
"""Noto CJK/DejaVu의 라이선스와 출처를 보존한 고정 폭 Skjáhermir 비트맵 skapa. 평상시 빌드는 vendor Skrá 사용."""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageDraw, ImageFont
verk_rót = Path(__file__).resolve().parents[1]


def Keyra_2():
    slóð_Listi = ['/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']
    leturgerð_Listi = [ImageFont.truetype(slóð_Listi[0], 13), ImageFont.truetype(slóð_Listi[1], 16, index=1), ImageFont.truetype(slóð_Listi[2], 16)]
    gögn = bytearray()
    for stafur_kóðun in list(range(65536)) + list(range(0x1f600, 0x1f650)):
        teikning_VALUE = Image.new('L', (16, 16)); 화면그리기 = ImageDraw.Draw(teikning_VALUE)
        if not (stafur_kóðun < 32 or 0xd800 <= stafur_kóðun <= 0xdfff):
            화면그리기.text((0, -1 if stafur_kóðun < 256 else -5 if stafur_kóðun < 65536 else -3), chr(stafur_kóðun), font=leturgerð_Listi[0 if stafur_kóðun < 256 else 1 if stafur_kóðun < 65536 else 2], fill=255)
        for Y_hnit in range(16):
            Background_Intelligent_Transfer_Service_Listi = 0
            for x_hnit in range(16): Background_Intelligent_Transfer_Service_Listi = Background_Intelligent_Transfer_Service_Listi * 2 + (teikning_VALUE.getpixel((x_hnit, Y_hnit)) >= 96)
            gögn += Background_Intelligent_Transfer_Service_Listi.to_bytes(2, 'big')
    markmið = verk_rót / 'vendor/terminal-font.bin'; markmið.write_bytes(gögn)
    이용허락목록 = [Path('/usr/share/doc/fonts-noto-cjk/copyright'), Path('/usr/share/doc/fonts-dejavu-core/copyright')]
    for 원본주소 in 이용허락목록: (verk_rót / 'vendor' / ('LICENSE.' + 원본주소.parent.name)).write_bytes(원본주소.read_bytes())
    (verk_rót / 'vendor/terminal-font.json').write_text(json.dumps({'name': 'JKOROS terminal bitmap', 'format': '16 rows, big-endian uint16 mask; BMP then U+1F600..1F64F', 'glyphs': 65536+80, 'sha256': hashlib.sha256(gögn).hexdigest(), 'sources': {gögn_staða: hashlib.sha256(Path(gögn_staða).read_bytes()).hexdigest() for gögn_staða in slóð_Listi}}, indent=2) + '\n')
    print(markmið)


if __name__ == '__main__': Keyra_2()
