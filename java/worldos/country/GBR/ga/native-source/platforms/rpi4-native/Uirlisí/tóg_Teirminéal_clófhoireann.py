#!/usr/bin/env python3
"""Noto CJK/DejaVu의 라이선스와 출처를 보존한 고정 폭 Teirminéal 비트맵 giniúint. 평상시 빌드는 vendor Comhad 사용."""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageDraw, ImageFont
teilgean_fréamh = Path(__file__).resolve().parents[1]


def Rith_2():
    cosán_Liosta = ['/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']
    clófhoireann_Liosta = [ImageFont.truetype(cosán_Liosta[0], 13), ImageFont.truetype(cosán_Liosta[1], 16, index=1), ImageFont.truetype(cosán_Liosta[2], 16)]
    sonraí = bytearray()
    for carachtar_ionchódú in list(range(65536)) + list(range(0x1f600, 0x1f650)):
        líníocht_VALUE = Image.new('L', (16, 16)); 화면그리기 = ImageDraw.Draw(líníocht_VALUE)
        if not (carachtar_ionchódú < 32 or 0xd800 <= carachtar_ionchódú <= 0xdfff):
            화면그리기.text((0, -1 if carachtar_ionchódú < 256 else -5 if carachtar_ionchódú < 65536 else -3), chr(carachtar_ionchódú), font=clófhoireann_Liosta[0 if carachtar_ionchódú < 256 else 1 if carachtar_ionchódú < 65536 else 2], fill=255)
        for 세로좌표 in range(16):
            비트들 = 0
            for x_chomhordanáid in range(16): 비트들 = 비트들 * 2 + (líníocht_VALUE.getpixel((x_chomhordanáid, 세로좌표)) >= 96)
            sonraí += 비트들.to_bytes(2, 'big')
    sprioc = teilgean_fréamh / 'vendor/terminal-font.bin'; sprioc.write_bytes(sonraí)
    이용허락목록 = [Path('/usr/share/doc/fonts-noto-cjk/copyright'), Path('/usr/share/doc/fonts-dejavu-core/copyright')]
    for 원본주소 in 이용허락목록: (teilgean_fréamh / 'vendor' / ('LICENSE.' + 원본주소.parent.name)).write_bytes(원본주소.read_bytes())
    (teilgean_fréamh / 'vendor/terminal-font.json').write_text(json.dumps({'name': 'JKOROS terminal bitmap', 'format': '16 rows, big-endian uint16 mask; BMP then U+1F600..1F64F', 'glyphs': 65536+80, 'sha256': hashlib.sha256(sonraí).hexdigest(), 'sources': {sonraí_suíomh: hashlib.sha256(Path(sonraí_suíomh).read_bytes()).hexdigest() for sonraí_suíomh in cosán_Liosta}}, indent=2) + '\n')
    print(sprioc)


if __name__ == '__main__': Rith_2()
