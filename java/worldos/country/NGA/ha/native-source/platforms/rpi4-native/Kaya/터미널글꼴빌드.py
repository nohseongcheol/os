#!/usr/bin/env python3
"""Noto CJK/DejaVu의 라이선스와 출처를 보존한 고정 폭 터미널 비트맵 생성. 평상시 빌드는 vendor Fayil 사용."""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageDraw, ImageFont
기준 = Path(__file__).resolve().parents[1]


def Tafiyar_da():
    Hanyar_shiga_Jeri = ['/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']
    salon_rubutu_Jeri = [ImageFont.truetype(Hanyar_shiga_Jeri[0], 13), ImageFont.truetype(Hanyar_shiga_Jeri[1], 16, index=1), ImageFont.truetype(Hanyar_shiga_Jeri[2], 16)]
    Tarin_bayani = bytearray()
    for Harafi_Juyar_da_bayanai_zuwa_lamba in list(range(65536)) + list(range(0x1f600, 0x1f650)):
        zane_Daraja = Image.new('L', (16, 16)); 화면그리기 = ImageDraw.Draw(zane_Daraja)
        if not (Harafi_Juyar_da_bayanai_zuwa_lamba < 32 or 0xd800 <= Harafi_Juyar_da_bayanai_zuwa_lamba <= 0xdfff):
            화면그리기.text((0, -1 if Harafi_Juyar_da_bayanai_zuwa_lamba < 256 else -5 if Harafi_Juyar_da_bayanai_zuwa_lamba < 65536 else -3), chr(Harafi_Juyar_da_bayanai_zuwa_lamba), font=salon_rubutu_Jeri[0 if Harafi_Juyar_da_bayanai_zuwa_lamba < 256 else 1 if Harafi_Juyar_da_bayanai_zuwa_lamba < 65536 else 2], fill=255)
        for Maɓallin_Y_Mai_tsarawa in range(16):
            Sabis_ɗin_Gusar_da_Tarin_Bayanan_Bayan_Bango_Jeri = 0
            for gamayyar_x in range(16): Sabis_ɗin_Gusar_da_Tarin_Bayanan_Bayan_Bango_Jeri = Sabis_ɗin_Gusar_da_Tarin_Bayanan_Bayan_Bango_Jeri * 2 + (zane_Daraja.getpixel((gamayyar_x, Maɓallin_Y_Mai_tsarawa)) >= 96)
            Tarin_bayani += Sabis_ɗin_Gusar_da_Tarin_Bayanan_Bayan_Bango_Jeri.to_bytes(2, 'big')
    tageti = 기준 / 'vendor/terminal-font.bin'; tageti.write_bytes(Tarin_bayani)
    이용허락목록 = [Path('/usr/share/doc/fonts-noto-cjk/copyright'), Path('/usr/share/doc/fonts-dejavu-core/copyright')]
    for 원본주소 in 이용허락목록: (기준 / 'vendor' / ('LICENSE.' + 원본주소.parent.name)).write_bytes(원본주소.read_bytes())
    (기준 / 'vendor/terminal-font.json').write_text(json.dumps({'name': 'JKOROS terminal bitmap', 'format': '16 rows, big-endian uint16 mask; BMP then U+1F600..1F64F', 'glyphs': 65536+80, 'sha256': hashlib.sha256(Tarin_bayani).hexdigest(), 'sources': {자료위치: hashlib.sha256(Path(자료위치).read_bytes()).hexdigest() for 자료위치 in Hanyar_shiga_Jeri}}, indent=2) + '\n')
    print(tageti)


if __name__ == '__main__': Tafiyar_da()
