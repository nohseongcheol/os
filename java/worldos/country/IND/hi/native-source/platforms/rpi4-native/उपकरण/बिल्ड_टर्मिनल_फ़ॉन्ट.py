#!/usr/bin/env python3
"""Noto CJK/DejaVu의 라이선스와 출처를 보존한 고정 폭 आदेशपटल 비트맵 जनरेट_करें. 평상시 빌드는 vendor संचिका 사용."""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageDraw, ImageFont
प्रोजेक्ट_करें_मूल = Path(__file__).resolve().parents[1]


def चलाएँ():
    पथ_सूची = ['/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']
    फ़ॉन्ट_सूची = [ImageFont.truetype(पथ_सूची[0], 13), ImageFont.truetype(पथ_सूची[1], 16, index=1), ImageFont.truetype(पथ_सूची[2], 16)]
    आँकड़े = bytearray()
    for वर्ण_एन्_कोडिंग in list(range(65536)) + list(range(0x1f600, 0x1f650)):
        ड्रॉइंग_मान = Image.new('L', (16, 16)); 화면그리기 = ImageDraw.Draw(ड्रॉइंग_मान)
        if not (वर्ण_एन्_कोडिंग < 32 or 0xd800 <= वर्ण_एन्_कोडिंग <= 0xdfff):
            화면그리기.text((0, -1 if वर्ण_एन्_कोडिंग < 256 else -5 if वर्ण_एन्_कोडिंग < 65536 else -3), chr(वर्ण_एन्_कोडिंग), font=फ़ॉन्ट_सूची[0 if वर्ण_एन्_कोडिंग < 256 else 1 if वर्ण_एन्_कोडिंग < 65536 else 2], fill=255)
        for 세로좌표 in range(16):
            बैकग्राउंड_इंटेलिजेंट_ट्रांसफ़र_सर्विस_सूची = 0
            for x_निर्देशांक in range(16): बैकग्राउंड_इंटेलिजेंट_ट्रांसफ़र_सर्विस_सूची = बैकग्राउंड_इंटेलिजेंट_ट्रांसफ़र_सर्विस_सूची * 2 + (ड्रॉइंग_मान.getpixel((x_निर्देशांक, 세로좌표)) >= 96)
            आँकड़े += बैकग्राउंड_इंटेलिजेंट_ट्रांसफ़र_सर्विस_सूची.to_bytes(2, 'big')
    लक्ष्य = प्रोजेक्ट_करें_मूल / 'vendor/terminal-font.bin'; लक्ष्य.write_bytes(आँकड़े)
    이용허락목록 = [Path('/usr/share/doc/fonts-noto-cjk/copyright'), Path('/usr/share/doc/fonts-dejavu-core/copyright')]
    for 원본주소 in 이용허락목록: (प्रोजेक्ट_करें_मूल / 'vendor' / ('LICENSE.' + 원본주소.parent.name)).write_bytes(원본주소.read_bytes())
    (प्रोजेक्ट_करें_मूल / 'vendor/terminal-font.json').write_text(json.dumps({'name': 'JKOROS terminal bitmap', 'format': '16 rows, big-endian uint16 mask; BMP then U+1F600..1F64F', 'glyphs': 65536+80, 'sha256': hashlib.sha256(आँकड़े).hexdigest(), 'sources': {डेटा_पद: hashlib.sha256(Path(डेटा_पद).read_bytes()).hexdigest() for डेटा_पद in पथ_सूची}}, indent=2) + '\n')
    print(लक्ष्य)


if __name__ == '__main__': चलाएँ()
