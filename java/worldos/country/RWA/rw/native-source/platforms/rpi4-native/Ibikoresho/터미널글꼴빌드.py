#!/usr/bin/env python3
"""Noto CJK/DejaVu의 라이선스와 출처를 보존한 고정 폭 터미널 비트맵 생성. 평상시 빌드는 vendor Idosiye 사용."""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageDraw, ImageFont
기준 = Path(__file__).resolve().parents[1]


def ihuriro():
    inzira_Urutonde = ['/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']
    imyandikire_Urutonde = [ImageFont.truetype(inzira_Urutonde[0], 13), ImageFont.truetype(inzira_Urutonde[1], 16, index=1), ImageFont.truetype(inzira_Urutonde[2], 16)]
    amakurushingiro = bytearray()
    for inyuguti_gusobeka in list(range(65536)) + list(range(0x1f600, 0x1f650)):
        igishushanyo_agaciro = Image.new('L', (16, 16)); 화면그리기 = ImageDraw.Draw(igishushanyo_agaciro)
        if not (inyuguti_gusobeka < 32 or 0xd800 <= inyuguti_gusobeka <= 0xdfff):
            화면그리기.text((0, -1 if inyuguti_gusobeka < 256 else -5 if inyuguti_gusobeka < 65536 else -3), chr(inyuguti_gusobeka), font=imyandikire_Urutonde[0 if inyuguti_gusobeka < 256 else 1 if inyuguti_gusobeka < 65536 else 2], fill=255)
        for 세로좌표 in range(16):
            비트들 = 0
            for Ihuza_rya_x in range(16): 비트들 = 비트들 * 2 + (igishushanyo_agaciro.getpixel((Ihuza_rya_x, 세로좌표)) >= 96)
            amakurushingiro += 비트들.to_bytes(2, 'big')
    gusimbuza_igishya = 기준 / 'vendor/terminal-font.bin'; gusimbuza_igishya.write_bytes(amakurushingiro)
    이용허락목록 = [Path('/usr/share/doc/fonts-noto-cjk/copyright'), Path('/usr/share/doc/fonts-dejavu-core/copyright')]
    for 원본주소 in 이용허락목록: (기준 / 'vendor' / ('LICENSE.' + 원본주소.parent.name)).write_bytes(원본주소.read_bytes())
    (기준 / 'vendor/terminal-font.json').write_text(json.dumps({'name': 'JKOROS terminal bitmap', 'format': '16 rows, big-endian uint16 mask; BMP then U+1F600..1F64F', 'glyphs': 65536+80, 'sha256': hashlib.sha256(amakurushingiro).hexdigest(), 'sources': {자료위치: hashlib.sha256(Path(자료위치).read_bytes()).hexdigest() for 자료위치 in inzira_Urutonde}}, indent=2) + '\n')
    print(gusimbuza_igishya)


if __name__ == '__main__': ihuriro()
