#!/usr/bin/env python3
"""Noto CJK/DejaVu의 라이선스와 출처를 보존한 고정 폭 Տերմինալ 비트맵 արտադրել. 평상시 빌드는 vendor Ֆայլ 사용."""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageDraw, ImageFont
արձակել_արմատ = Path(__file__).resolve().parents[1]


def Գործարկել():
    ուղի_Ցուցակ = ['/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']
    տառատեսակ_Ցուցակ = [ImageFont.truetype(ուղի_Ցուցակ[0], 13), ImageFont.truetype(ուղի_Ցուցակ[1], 16, index=1), ImageFont.truetype(ուղի_Ցուցակ[2], 16)]
    տվյալ = bytearray()
    for գրանշան_կոդավորում in list(range(65536)) + list(range(0x1f600, 0x1f650)):
        նկար_արժեք_c143fe9e = Image.new('L', (16, 16)); 화면그리기 = ImageDraw.Draw(նկար_արժեք_c143fe9e)
        if not (գրանշան_կոդավորում < 32 or 0xd800 <= գրանշան_կոդավորում <= 0xdfff):
            화면그리기.text((0, -1 if գրանշան_կոդավորում < 256 else -5 if գրանշան_կոդավորում < 65536 else -3), chr(գրանշան_կոդավորում), font=տառատեսակ_Ցուցակ[0 if գրանշան_կոդավորում < 256 else 1 if գրանշան_կոդավորում < 65536 else 2], fill=255)
        for 세로좌표 in range(16):
            비트들 = 0
            for x_կոորդինատ in range(16): 비트들 = 비트들 * 2 + (նկար_արժեք_c143fe9e.getpixel((x_կոորդինատ, 세로좌표)) >= 96)
            տվյալ += 비트들.to_bytes(2, 'big')
    թիրախ = արձակել_արմատ / 'vendor/terminal-font.bin'; թիրախ.write_bytes(տվյալ)
    이용허락목록 = [Path('/usr/share/doc/fonts-noto-cjk/copyright'), Path('/usr/share/doc/fonts-dejavu-core/copyright')]
    for 원본주소 in 이용허락목록: (արձակել_արմատ / 'vendor' / ('LICENSE.' + 원본주소.parent.name)).write_bytes(원본주소.read_bytes())
    (արձակել_արմատ / 'vendor/terminal-font.json').write_text(json.dumps({'name': 'JKOROS terminal bitmap', 'format': '16 rows, big-endian uint16 mask; BMP then U+1F600..1F64F', 'glyphs': 65536+80, 'sha256': hashlib.sha256(տվյալ).hexdigest(), 'sources': {տվյալ_դիրք: hashlib.sha256(Path(տվյալ_դիրք).read_bytes()).hexdigest() for տվյալ_դիրք in ուղի_Ցուցակ}}, indent=2) + '\n')
    print(թիրախ)


if __name__ == '__main__': Գործարկել()
