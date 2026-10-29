#!/usr/bin/env python3
"""Noto CJK/DejaVu의 라이선스와 출처를 보존한 고정 폭 terminal 비트맵 genereerima. 평상시 빌드는 vendor Fail kasutus_VALUE."""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageDraw, ImageFont
Project_juur = Path(__file__).resolve().parents[1]


def Käivita_2():
    tee_Loend = ['/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']
    font_Loend = [ImageFont.truetype(tee_Loend[0], 13), ImageFont.truetype(tee_Loend[1], 16, index=1), ImageFont.truetype(tee_Loend[2], 16)]
    andmed = bytearray()
    for märk_kodeerimine in list(range(65536)) + list(range(0x1f600, 0x1f650)):
        joonis_VALUE = Image.new('L', (16, 16)); 화면그리기 = ImageDraw.Draw(joonis_VALUE)
        if not (märk_kodeerimine < 32 or 0xd800 <= märk_kodeerimine <= 0xdfff):
            화면그리기.text((0, -1 if märk_kodeerimine < 256 else -5 if märk_kodeerimine < 65536 else -3), chr(märk_kodeerimine), font=font_Loend[0 if märk_kodeerimine < 256 else 1 if märk_kodeerimine < 65536 else 2], fill=255)
        for 세로좌표 in range(16):
            Taustal_töötav_intelligentne_edastusteenus_Loend = 0
            for 가로좌표 in range(16): Taustal_töötav_intelligentne_edastusteenus_Loend = Taustal_töötav_intelligentne_edastusteenus_Loend * 2 + (joonis_VALUE.getpixel((가로좌표, 세로좌표)) >= 96)
            andmed += Taustal_töötav_intelligentne_edastusteenus_Loend.to_bytes(2, 'big')
    siht = Project_juur / 'vendor/terminal-font.bin'; siht.write_bytes(andmed)
    이용허락목록 = [Path('/usr/share/doc/fonts-noto-cjk/copyright'), Path('/usr/share/doc/fonts-dejavu-core/copyright')]
    for 원본주소 in 이용허락목록: (Project_juur / 'vendor' / ('LICENSE.' + 원본주소.parent.name)).write_bytes(원본주소.read_bytes())
    (Project_juur / 'vendor/terminal-font.json').write_text(json.dumps({'name': 'JKOROS terminal bitmap', 'format': '16 rows, big-endian uint16 mask; BMP then U+1F600..1F64F', 'glyphs': 65536+80, 'sha256': hashlib.sha256(andmed).hexdigest(), 'sources': {andmed_ametikoht: hashlib.sha256(Path(andmed_ametikoht).read_bytes()).hexdigest() for andmed_ametikoht in tee_Loend}}, indent=2) + '\n')
    print(siht)


if __name__ == '__main__': Käivita_2()
