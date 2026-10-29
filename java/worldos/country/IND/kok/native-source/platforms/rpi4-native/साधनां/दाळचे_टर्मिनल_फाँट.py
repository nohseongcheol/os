#!/usr/bin/env python3
"""Noto CJK/DejaVu의 라이선스와 출처를 보존한 고정 폭 टर्मिनल 비트맵 तयार_करचें. 평상시 빌드는 vendor फायल 사용."""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageDraw, ImageFont
प्रॉजॅक्ट_रूट = Path(__file__).resolve().parents[1]


def चलोवप():
    पाथ_सुची = ['/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']
    फाँट_सुची = [ImageFont.truetype(पाथ_सुची[0], 13), ImageFont.truetype(पाथ_सुची[1], 16, index=1), ImageFont.truetype(पाथ_सुची[2], 16)]
    डेटा = bytearray()
    for वर्ण_एनकोडिंग in list(range(65536)) + list(range(0x1f600, 0x1f650)):
        रेखाटन_मोल = Image.new('L', (16, 16)); 화면그리기 = ImageDraw.Draw(रेखाटन_मोल)
        if not (वर्ण_एनकोडिंग < 32 or 0xd800 <= वर्ण_एनकोडिंग <= 0xdfff):
            화면그리기.text((0, -1 if वर्ण_एनकोडिंग < 256 else -5 if वर्ण_एनकोडिंग < 65536 else -3), chr(वर्ण_एनकोडिंग), font=फाँट_सुची[0 if वर्ण_एनकोडिंग < 256 else 1 if वर्ण_एनकोडिंग < 65536 else 2], fill=255)
        for 세로좌표 in range(16):
            비트들 = 0
            for x_coordinate in range(16): 비트들 = 비트들 * 2 + (रेखाटन_मोल.getpixel((x_coordinate, 세로좌표)) >= 96)
            डेटा += 비트들.to_bytes(2, 'big')
    लक्ष्य = प्रॉजॅक्ट_रूट / 'vendor/terminal-font.bin'; लक्ष्य.write_bytes(डेटा)
    이용허락목록 = [Path('/usr/share/doc/fonts-noto-cjk/copyright'), Path('/usr/share/doc/fonts-dejavu-core/copyright')]
    for 원본주소 in 이용허락목록: (प्रॉजॅक्ट_रूट / 'vendor' / ('LICENSE.' + 원본주소.parent.name)).write_bytes(원본주소.read_bytes())
    (प्रॉजॅक्ट_रूट / 'vendor/terminal-font.json').write_text(json.dumps({'name': 'JKOROS terminal bitmap', 'format': '16 rows, big-endian uint16 mask; BMP then U+1F600..1F64F', 'glyphs': 65536+80, 'sha256': hashlib.sha256(डेटा).hexdigest(), 'sources': {डेटा_स्थिती: hashlib.sha256(Path(डेटा_स्थिती).read_bytes()).hexdigest() for डेटा_स्थिती in पाथ_सुची}}, indent=2) + '\n')
    print(लक्ष्य)


if __name__ == '__main__': चलोवप()
