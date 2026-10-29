#!/usr/bin/env python3
"""Noto CJK/DejaVu의 라이선스와 출처를 보존한 고정 폭 Terminali 비트맵 gjeneroj. 평상시 빌드는 vendor Kartelë 사용."""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageDraw, ImageFont
Project_rrënjë = Path(__file__).resolve().parents[1]


def Ekzekuto():
    shteg_Listë = ['/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']
    font_Listë = [ImageFont.truetype(shteg_Listë[0], 13), ImageFont.truetype(shteg_Listë[1], 16, index=1), ImageFont.truetype(shteg_Listë[2], 16)]
    të_dhëna = bytearray()
    for karakter_enkodim in list(range(65536)) + list(range(0x1f600, 0x1f650)):
        vizatim_VALUE = Image.new('L', (16, 16)); 화면그리기 = ImageDraw.Draw(vizatim_VALUE)
        if not (karakter_enkodim < 32 or 0xd800 <= karakter_enkodim <= 0xdfff):
            화면그리기.text((0, -1 if karakter_enkodim < 256 else -5 if karakter_enkodim < 65536 else -3), chr(karakter_enkodim), font=font_Listë[0 if karakter_enkodim < 256 else 1 if karakter_enkodim < 65536 else 2], fill=255)
        for Y_koordinatë in range(16):
            Shërbimi_i_transferimit_inteligjent_në_sfond_Listë = 0
            for koordinata_x in range(16): Shërbimi_i_transferimit_inteligjent_në_sfond_Listë = Shërbimi_i_transferimit_inteligjent_në_sfond_Listë * 2 + (vizatim_VALUE.getpixel((koordinata_x, Y_koordinatë)) >= 96)
            të_dhëna += Shërbimi_i_transferimit_inteligjent_në_sfond_Listë.to_bytes(2, 'big')
    objektiv = Project_rrënjë / 'vendor/terminal-font.bin'; objektiv.write_bytes(të_dhëna)
    이용허락목록 = [Path('/usr/share/doc/fonts-noto-cjk/copyright'), Path('/usr/share/doc/fonts-dejavu-core/copyright')]
    for 원본주소 in 이용허락목록: (Project_rrënjë / 'vendor' / ('LICENSE.' + 원본주소.parent.name)).write_bytes(원본주소.read_bytes())
    (Project_rrënjë / 'vendor/terminal-font.json').write_text(json.dumps({'name': 'JKOROS terminal bitmap', 'format': '16 rows, big-endian uint16 mask; BMP then U+1F600..1F64F', 'glyphs': 65536+80, 'sha256': hashlib.sha256(të_dhëna).hexdigest(), 'sources': {të_dhëna_pozicioni: hashlib.sha256(Path(të_dhëna_pozicioni).read_bytes()).hexdigest() for të_dhëna_pozicioni in shteg_Listë}}, indent=2) + '\n')
    print(objektiv)


if __name__ == '__main__': Ekzekuto()
