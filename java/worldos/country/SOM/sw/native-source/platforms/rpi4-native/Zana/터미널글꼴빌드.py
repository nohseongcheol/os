#!/usr/bin/env python3
"""Noto CJK/DejaVu의 라이선스와 출처를 보존한 고정 폭 터미널 비트맵 생성. 평상시 빌드는 vendor faili 사용."""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageDraw, ImageFont
기준 = Path(__file__).resolve().parents[1]


def endesha():
    njia_Orodha = ['/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']
    fonti_Orodha = [ImageFont.truetype(njia_Orodha[0], 13), ImageFont.truetype(njia_Orodha[1], 16, index=1), ImageFont.truetype(njia_Orodha[2], 16)]
    data = bytearray()
    for kibambo_usimbaji in list(range(65536)) + list(range(0x1f600, 0x1f650)):
        mchoro_thamani = Image.new('L', (16, 16)); 화면그리기 = ImageDraw.Draw(mchoro_thamani)
        if not (kibambo_usimbaji < 32 or 0xd800 <= kibambo_usimbaji <= 0xdfff):
            화면그리기.text((0, -1 if kibambo_usimbaji < 256 else -5 if kibambo_usimbaji < 65536 else -3), chr(kibambo_usimbaji), font=fonti_Orodha[0 if kibambo_usimbaji < 256 else 1 if kibambo_usimbaji < 65536 else 2], fill=255)
        for Kitufe_cha_Y_kiratibu in range(16):
            Huduma_ya_Uhamisho_wa_Ujasusi_wa_Mandharinyuma_Orodha = 0
            for jira_x in range(16): Huduma_ya_Uhamisho_wa_Ujasusi_wa_Mandharinyuma_Orodha = Huduma_ya_Uhamisho_wa_Ujasusi_wa_Mandharinyuma_Orodha * 2 + (mchoro_thamani.getpixel((jira_x, Kitufe_cha_Y_kiratibu)) >= 96)
            data += Huduma_ya_Uhamisho_wa_Ujasusi_wa_Mandharinyuma_Orodha.to_bytes(2, 'big')
    lengo = 기준 / 'vendor/terminal-font.bin'; lengo.write_bytes(data)
    이용허락목록 = [Path('/usr/share/doc/fonts-noto-cjk/copyright'), Path('/usr/share/doc/fonts-dejavu-core/copyright')]
    for 원본주소 in 이용허락목록: (기준 / 'vendor' / ('LICENSE.' + 원본주소.parent.name)).write_bytes(원본주소.read_bytes())
    (기준 / 'vendor/terminal-font.json').write_text(json.dumps({'name': 'JKOROS terminal bitmap', 'format': '16 rows, big-endian uint16 mask; BMP then U+1F600..1F64F', 'glyphs': 65536+80, 'sha256': hashlib.sha256(data).hexdigest(), 'sources': {자료위치: hashlib.sha256(Path(자료위치).read_bytes()).hexdigest() for 자료위치 in njia_Orodha}}, indent=2) + '\n')
    print(lengo)


if __name__ == '__main__': endesha()
