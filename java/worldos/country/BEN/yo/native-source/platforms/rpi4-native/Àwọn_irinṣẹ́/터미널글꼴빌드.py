#!/usr/bin/env python3
"""Noto CJK/DejaVu의 라이선스와 출처를 보존한 고정 폭 터미널 비트맵 생성. 평상시 빌드는 vendor Fáìlì 사용."""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageDraw, ImageFont
기준 = Path(__file__).resolve().parents[1]


def Rọ́ọ̀nù():
    ọ̀nà_Àtòkọ = ['/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']
    ìrísí_lẹ́tà_Àtòkọ = [ImageFont.truetype(ọ̀nà_Àtòkọ[0], 13), ImageFont.truetype(ọ̀nà_Àtòkọ[1], 16, index=1), ImageFont.truetype(ọ̀nà_Àtòkọ[2], 16)]
    détà = bytearray()
    for ẹyọ_ọ̀rọ̀_pípàrokò in list(range(65536)) + list(range(0x1f600, 0x1f650)):
        íyàwòrán_iye = Image.new('L', (16, 16)); 화면그리기 = ImageDraw.Draw(íyàwòrán_iye)
        if not (ẹyọ_ọ̀rọ̀_pípàrokò < 32 or 0xd800 <= ẹyọ_ọ̀rọ̀_pípàrokò <= 0xdfff):
            화면그리기.text((0, -1 if ẹyọ_ọ̀rọ̀_pípàrokò < 256 else -5 if ẹyọ_ọ̀rọ̀_pípàrokò < 65536 else -3), chr(ẹyọ_ọ̀rọ̀_pípàrokò), font=ìrísí_lẹ́tà_Àtòkọ[0 if ẹyọ_ọ̀rọ̀_pípàrokò < 256 else 1 if ẹyọ_ọ̀rọ̀_pípàrokò < 65536 else 2], fill=255)
        for 세로좌표 in range(16):
            비트들 = 0
            for ibi_ìtọ́kasí_x in range(16): 비트들 = 비트들 * 2 + (íyàwòrán_iye.getpixel((ibi_ìtọ́kasí_x, 세로좌표)) >= 96)
            détà += 비트들.to_bytes(2, 'big')
    àfojúsùn = 기준 / 'vendor/terminal-font.bin'; àfojúsùn.write_bytes(détà)
    이용허락목록 = [Path('/usr/share/doc/fonts-noto-cjk/copyright'), Path('/usr/share/doc/fonts-dejavu-core/copyright')]
    for 원본주소 in 이용허락목록: (기준 / 'vendor' / ('LICENSE.' + 원본주소.parent.name)).write_bytes(원본주소.read_bytes())
    (기준 / 'vendor/terminal-font.json').write_text(json.dumps({'name': 'JKOROS terminal bitmap', 'format': '16 rows, big-endian uint16 mask; BMP then U+1F600..1F64F', 'glyphs': 65536+80, 'sha256': hashlib.sha256(détà).hexdigest(), 'sources': {자료위치: hashlib.sha256(Path(자료위치).read_bytes()).hexdigest() for 자료위치 in ọ̀nà_Àtòkọ}}, indent=2) + '\n')
    print(àfojúsùn)


if __name__ == '__main__': Rọ́ọ̀nù()
