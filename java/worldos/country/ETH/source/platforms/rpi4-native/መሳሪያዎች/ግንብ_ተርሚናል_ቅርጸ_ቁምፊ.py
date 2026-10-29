#!/usr/bin/env python3
"""Noto CJK/DejaVu의 라이선스와 출처를 보존한 고정 폭 ተርሚናል 비트맵 አዘጋጅ. 평상시 빌드는 vendor ፋይል 사용."""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageDraw, ImageFont
አሳይ_ስር = Path(__file__).resolve().parents[1]


def ማስኬጃ():
    ዱካ_ዝርዝር = ['/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']
    ቅርጸ_ቁምፊ_ዝርዝር = [ImageFont.truetype(ዱካ_ዝርዝር[0], 13), ImageFont.truetype(ዱካ_ዝርዝር[1], 16, index=1), ImageFont.truetype(ዱካ_ዝርዝር[2], 16)]
    ውሂብ = bytearray()
    for ቁምፊ_በኮድ_መክተት in list(range(65536)) + list(range(0x1f600, 0x1f650)):
        ስዕል_እሴት = Image.new('L', (16, 16)); 화면그리기 = ImageDraw.Draw(ስዕል_እሴት)
        if not (ቁምፊ_በኮድ_መክተት < 32 or 0xd800 <= ቁምፊ_በኮድ_መክተት <= 0xdfff):
            화면그리기.text((0, -1 if ቁምፊ_በኮድ_መክተት < 256 else -5 if ቁምፊ_በኮድ_መክተት < 65536 else -3), chr(ቁምፊ_በኮድ_መክተት), font=ቅርጸ_ቁምፊ_ዝርዝር[0 if ቁምፊ_በኮድ_መክተት < 256 else 1 if ቁምፊ_በኮድ_መክተት < 65536 else 2], fill=255)
        for 세로좌표 in range(16):
            የበስተጀርባ_ብልህ_የማስተላለፍ_አገልግሎት_ዝርዝር = 0
            for ኤክስ_አስተባባሪ in range(16): የበስተጀርባ_ብልህ_የማስተላለፍ_አገልግሎት_ዝርዝር = የበስተጀርባ_ብልህ_የማስተላለፍ_አገልግሎት_ዝርዝር * 2 + (ስዕል_እሴት.getpixel((ኤክስ_አስተባባሪ, 세로좌표)) >= 96)
            ውሂብ += የበስተጀርባ_ብልህ_የማስተላለፍ_አገልግሎት_ዝርዝር.to_bytes(2, 'big')
    ዓላማ = አሳይ_ስር / 'vendor/terminal-font.bin'; ዓላማ.write_bytes(ውሂብ)
    이용허락목록 = [Path('/usr/share/doc/fonts-noto-cjk/copyright'), Path('/usr/share/doc/fonts-dejavu-core/copyright')]
    for 원본주소 in 이용허락목록: (አሳይ_ስር / 'vendor' / ('LICENSE.' + 원본주소.parent.name)).write_bytes(원본주소.read_bytes())
    (አሳይ_ስር / 'vendor/terminal-font.json').write_text(json.dumps({'name': 'JKOROS terminal bitmap', 'format': '16 rows, big-endian uint16 mask; BMP then U+1F600..1F64F', 'glyphs': 65536+80, 'sha256': hashlib.sha256(ውሂብ).hexdigest(), 'sources': {ውሂብ_በቦታ_አስቀመጠ: hashlib.sha256(Path(ውሂብ_በቦታ_አስቀመጠ).read_bytes()).hexdigest() for ውሂብ_በቦታ_አስቀመጠ in ዱካ_ዝርዝር}}, indent=2) + '\n')
    print(ዓላማ)


if __name__ == '__main__': ማስኬጃ()
