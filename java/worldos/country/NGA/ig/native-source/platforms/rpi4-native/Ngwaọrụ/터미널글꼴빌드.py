#!/usr/bin/env python3
"""Noto CJK/DejaVu의 라이선스와 출처를 보존한 고정 폭 터미널 비트맵 생성. 평상시 빌드는 vendor Faịlụ 사용."""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageDraw, ImageFont
기준 = Path(__file__).resolve().parents[1]


def Bido():
    ụzọ_ozi_ndepụta = ['/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']
    ọnụndèe_ndepụta = [ImageFont.truetype(ụzọ_ozi_ndepụta[0], 13), ImageFont.truetype(ụzọ_ozi_ndepụta[1], 16, index=1), ImageFont.truetype(ụzọ_ozi_ndepụta[2], 16)]
    datà = bytearray()
    for mkpụrụedemede_ntinye_koòdù in list(range(65536)) + list(range(0x1f600, 0x1f650)):
        osise_valuu = Image.new('L', (16, 16)); 화면그리기 = ImageDraw.Draw(osise_valuu)
        if not (mkpụrụedemede_ntinye_koòdù < 32 or 0xd800 <= mkpụrụedemede_ntinye_koòdù <= 0xdfff):
            화면그리기.text((0, -1 if mkpụrụedemede_ntinye_koòdù < 256 else -5 if mkpụrụedemede_ntinye_koòdù < 65536 else -3), chr(mkpụrụedemede_ntinye_koòdù), font=ọnụndèe_ndepụta[0 if mkpụrụedemede_ntinye_koòdù < 256 else 1 if mkpụrụedemede_ntinye_koòdù < 65536 else 2], fill=255)
        for 세로좌표 in range(16):
            비트들 = 0
            for ngakọrịta_x in range(16): 비트들 = 비트들 * 2 + (osise_valuu.getpixel((ngakọrịta_x, 세로좌표)) >= 96)
            datà += 비트들.to_bytes(2, 'big')
    ebenlereanya = 기준 / 'vendor/terminal-font.bin'; ebenlereanya.write_bytes(datà)
    이용허락목록 = [Path('/usr/share/doc/fonts-noto-cjk/copyright'), Path('/usr/share/doc/fonts-dejavu-core/copyright')]
    for 원본주소 in 이용허락목록: (기준 / 'vendor' / ('LICENSE.' + 원본주소.parent.name)).write_bytes(원본주소.read_bytes())
    (기준 / 'vendor/terminal-font.json').write_text(json.dumps({'name': 'JKOROS terminal bitmap', 'format': '16 rows, big-endian uint16 mask; BMP then U+1F600..1F64F', 'glyphs': 65536+80, 'sha256': hashlib.sha256(datà).hexdigest(), 'sources': {자료위치: hashlib.sha256(Path(자료위치).read_bytes()).hexdigest() for 자료위치 in ụzọ_ozi_ndepụta}}, indent=2) + '\n')
    print(ebenlereanya)


if __name__ == '__main__': Bido()
