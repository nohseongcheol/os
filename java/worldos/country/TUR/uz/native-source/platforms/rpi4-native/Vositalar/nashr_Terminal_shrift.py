#!/usr/bin/env python3
"""Noto CJK/DejaVu의 라이선스와 출처를 보존한 고정 폭 Terminal 비트맵 generatsiiyalash. 평상시 빌드는 vendor Fayl 사용."""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageDraw, ImageFont
Project_ildiz = Path(__file__).resolve().parents[1]


def Bajarish():
    yo_l_Ro_yxat = ['/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']
    shrift_Ro_yxat = [ImageFont.truetype(yo_l_Ro_yxat[0], 13), ImageFont.truetype(yo_l_Ro_yxat[1], 16, index=1), ImageFont.truetype(yo_l_Ro_yxat[2], 16)]
    ma_lumotlar = bytearray()
    for belgi_kodlash in list(range(65536)) + list(range(0x1f600, 0x1f650)):
        chizish_VALUE = Image.new('L', (16, 16)); 화면그리기 = ImageDraw.Draw(chizish_VALUE)
        if not (belgi_kodlash < 32 or 0xd800 <= belgi_kodlash <= 0xdfff):
            화면그리기.text((0, -1 if belgi_kodlash < 256 else -5 if belgi_kodlash < 65536 else -3), chr(belgi_kodlash), font=shrift_Ro_yxat[0 if belgi_kodlash < 256 else 1 if belgi_kodlash < 65536 else 2], fill=255)
        for Y_tugmasi_koordinat in range(16):
            fonda_intellektual_uzatish_xizmati_Ro_yxat = 0
            for x_koordinata in range(16): fonda_intellektual_uzatish_xizmati_Ro_yxat = fonda_intellektual_uzatish_xizmati_Ro_yxat * 2 + (chizish_VALUE.getpixel((x_koordinata, Y_tugmasi_koordinat)) >= 96)
            ma_lumotlar += fonda_intellektual_uzatish_xizmati_Ro_yxat.to_bytes(2, 'big')
    nishon = Project_ildiz / 'vendor/terminal-font.bin'; nishon.write_bytes(ma_lumotlar)
    이용허락목록 = [Path('/usr/share/doc/fonts-noto-cjk/copyright'), Path('/usr/share/doc/fonts-dejavu-core/copyright')]
    for 원본주소 in 이용허락목록: (Project_ildiz / 'vendor' / ('LICENSE.' + 원본주소.parent.name)).write_bytes(원본주소.read_bytes())
    (Project_ildiz / 'vendor/terminal-font.json').write_text(json.dumps({'name': 'JKOROS terminal bitmap', 'format': '16 rows, big-endian uint16 mask; BMP then U+1F600..1F64F', 'glyphs': 65536+80, 'sha256': hashlib.sha256(ma_lumotlar).hexdigest(), 'sources': {ma_lumotlar_holat: hashlib.sha256(Path(ma_lumotlar_holat).read_bytes()).hexdigest() for ma_lumotlar_holat in yo_l_Ro_yxat}}, indent=2) + '\n')
    print(nishon)


if __name__ == '__main__': Bajarish()
