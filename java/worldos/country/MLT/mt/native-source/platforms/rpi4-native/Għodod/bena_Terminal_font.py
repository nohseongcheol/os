#!/usr/bin/env python3
"""Noto CJK/DejaVu의 라이선스와 출처를 보존한 고정 폭 Terminal 비트맵 iġġenera. 평상시 빌드는 vendor fajl 사용."""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageDraw, ImageFont
pprojetta_għerq = Path(__file__).resolve().parents[1]


def serje():
    mogħdija_Lista = ['/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']
    font_Lista = [ImageFont.truetype(mogħdija_Lista[0], 13), ImageFont.truetype(mogħdija_Lista[1], 16, index=1), ImageFont.truetype(mogħdija_Lista[2], 16)]
    data = bytearray()
    for karattru_kodifikar in list(range(65536)) + list(range(0x1f600, 0x1f650)):
        tpinġija_VALUE = Image.new('L', (16, 16)); 화면그리기 = ImageDraw.Draw(tpinġija_VALUE)
        if not (karattru_kodifikar < 32 or 0xd800 <= karattru_kodifikar <= 0xdfff):
            화면그리기.text((0, -1 if karattru_kodifikar < 256 else -5 if karattru_kodifikar < 65536 else -3), chr(karattru_kodifikar), font=font_Lista[0 if karattru_kodifikar < 256 else 1 if karattru_kodifikar < 65536 else 2], fill=255)
        for 세로좌표 in range(16):
            비트들 = 0
            for koordinat_x in range(16): 비트들 = 비트들 * 2 + (tpinġija_VALUE.getpixel((koordinat_x, 세로좌표)) >= 96)
            data += 비트들.to_bytes(2, 'big')
    mira = pprojetta_għerq / 'vendor/terminal-font.bin'; mira.write_bytes(data)
    이용허락목록 = [Path('/usr/share/doc/fonts-noto-cjk/copyright'), Path('/usr/share/doc/fonts-dejavu-core/copyright')]
    for 원본주소 in 이용허락목록: (pprojetta_għerq / 'vendor' / ('LICENSE.' + 원본주소.parent.name)).write_bytes(원본주소.read_bytes())
    (pprojetta_għerq / 'vendor/terminal-font.json').write_text(json.dumps({'name': 'JKOROS terminal bitmap', 'format': '16 rows, big-endian uint16 mask; BMP then U+1F600..1F64F', 'glyphs': 65536+80, 'sha256': hashlib.sha256(data).hexdigest(), 'sources': {data_pożizzjoni: hashlib.sha256(Path(data_pożizzjoni).read_bytes()).hexdigest() for data_pożizzjoni in mogħdija_Lista}}, indent=2) + '\n')
    print(mira)


if __name__ == '__main__': serje()
