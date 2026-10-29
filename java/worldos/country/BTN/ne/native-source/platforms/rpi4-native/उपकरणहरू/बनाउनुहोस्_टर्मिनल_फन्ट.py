#!/usr/bin/env python3
"""Noto CJK/DejaVu의 라이선스와 출처를 보존한 고정 폭 टर्मिनल 비트맵 सिर्जना_गर्नुहोस्. 평상시 빌드는 vendor फाइल 사용."""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageDraw, ImageFont
परियोजना_रूट = Path(__file__).resolve().parents[1]


def चलाउनुहोस्():
    बाटो_सूची = ['/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']
    फन्ट_सूची = [ImageFont.truetype(बाटो_सूची[0], 13), ImageFont.truetype(बाटो_सूची[1], 16, index=1), ImageFont.truetype(बाटो_सूची[2], 16)]
    लगत = bytearray()
    for वर्ण_एनकोडिङ in list(range(65536)) + list(range(0x1f600, 0x1f650)):
        चित्रकारी_मान = Image.new('L', (16, 16)); 화면그리기 = ImageDraw.Draw(चित्रकारी_मान)
        if not (वर्ण_एनकोडिङ < 32 or 0xd800 <= वर्ण_एनकोडिङ <= 0xdfff):
            화면그리기.text((0, -1 if वर्ण_एनकोडिङ < 256 else -5 if वर्ण_एनकोडिङ < 65536 else -3), chr(वर्ण_एनकोडिङ), font=फन्ट_सूची[0 if वर्ण_एनकोडिङ < 256 else 1 if वर्ण_एनकोडिङ < 65536 else 2], fill=255)
        for 세로좌표 in range(16):
            비트들 = 0
            for x_समन्वय in range(16): 비트들 = 비트들 * 2 + (चित्रकारी_मान.getpixel((x_समन्वय, 세로좌표)) >= 96)
            लगत += 비트들.to_bytes(2, 'big')
    लक्ष्य = परियोजना_रूट / 'vendor/terminal-font.bin'; लक्ष्य.write_bytes(लगत)
    이용허락목록 = [Path('/usr/share/doc/fonts-noto-cjk/copyright'), Path('/usr/share/doc/fonts-dejavu-core/copyright')]
    for 원본주소 in 이용허락목록: (परियोजना_रूट / 'vendor' / ('LICENSE.' + 원본주소.parent.name)).write_bytes(원본주소.read_bytes())
    (परियोजना_रूट / 'vendor/terminal-font.json').write_text(json.dumps({'name': 'JKOROS terminal bitmap', 'format': '16 rows, big-endian uint16 mask; BMP then U+1F600..1F64F', 'glyphs': 65536+80, 'sha256': hashlib.sha256(लगत).hexdigest(), 'sources': {लगत_राख्नुहोस्: hashlib.sha256(Path(लगत_राख्नुहोस्).read_bytes()).hexdigest() for लगत_राख्नुहोस् in बाटो_सूची}}, indent=2) + '\n')
    print(लक्ष्य)


if __name__ == '__main__': चलाउनुहोस्()
