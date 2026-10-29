#!/usr/bin/env python3
"""Noto CJK/DejaVu의 라이선스와 출처를 보존한 고정 रुंदी_विस्तार टर्मिनल 비트맵 तयार_करा. 평상시 빌드는 vendor फाइल वापर_मूल्य."""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageDraw, ImageFont
प्रोजेक्ट_मूळ = Path(__file__).resolve().parents[1]


def सुरू_करा():
    पथ_यादी = ['/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']
    फॉन्ट_यादी = [ImageFont.truetype(पथ_यादी[0], 13), ImageFont.truetype(पथ_यादी[1], 16, index=1), ImageFont.truetype(पथ_यादी[2], 16)]
    डेटा = bytearray()
    for वर्ण_एन्कोडिंग in list(range(65536)) + list(range(0x1f600, 0x1f650)):
        रेखांकन_मूल्य = Image.new('L', (16, 16)); पडदा_आरेखित_करा = ImageDraw.Draw(रेखांकन_मूल्य)
        if not (वर्ण_एन्कोडिंग < 32 or 0xd800 <= वर्ण_एन्कोडिंग <= 0xdfff):
            पडदा_आरेखित_करा.text((0, -1 if वर्ण_एन्कोडिंग < 256 else -5 if वर्ण_एन्कोडिंग < 65536 else -3), chr(वर्ण_एन्कोडिंग), font=फॉन्ट_यादी[0 if वर्ण_एन्कोडिंग < 256 else 1 if वर्ण_एन्कोडिंग < 65536 else 2], fill=255)
        for उभे_समन्वयीत in range(16):
            द्व्यंक_यादी = 0
            for आडवे_समन्वयीत in range(16): द्व्यंक_यादी = द्व्यंक_यादी * 2 + (रेखांकन_मूल्य.getpixel((आडवे_समन्वयीत, उभे_समन्वयीत)) >= 96)
            डेटा += द्व्यंक_यादी.to_bytes(2, 'big')
    लक्ष्य = प्रोजेक्ट_मूळ / 'vendor/terminal-font.bin'; लक्ष्य.write_bytes(डेटा)
    परवाने = [Path('/usr/share/doc/fonts-noto-cjk/copyright'), Path('/usr/share/doc/fonts-dejavu-core/copyright')]
    for मूळ_पत्ता_4c9bece9 in परवाने: (प्रोजेक्ट_मूळ / 'vendor' / ('LICENSE.' + मूळ_पत्ता_4c9bece9.parent.name)).write_bytes(मूळ_पत्ता_4c9bece9.read_bytes())
    (प्रोजेक्ट_मूळ / 'vendor/terminal-font.json').write_text(json.dumps({'name': 'JKOROS terminal bitmap', 'format': '16 rows, big-endian uint16 mask; BMP then U+1F600..1F64F', 'glyphs': 65536+80, 'sha256': hashlib.sha256(डेटा).hexdigest(), 'sources': {डेटा_स्थान: hashlib.sha256(Path(डेटा_स्थान).read_bytes()).hexdigest() for डेटा_स्थान in पथ_यादी}}, indent=2) + '\n')
    print(लक्ष्य)


if __name__ == '__main__': सुरू_करा()
