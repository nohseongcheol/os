#!/usr/bin/env python3
"""Noto CJK/DejaVu의 라이선스와 출처를 보존한 고정 폭 టెర్మినల్ 비트맵 రూపొందించు. 평상시 빌드는 vendor దస్త్రం 사용."""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageDraw, ImageFont
ప్రొజెక్ట్_మూలం = Path(__file__).resolve().parents[1]


def నడుపుము():
    పథం_జాబితా = ['/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']
    అక్షరాకృతి_జాబితా = [ImageFont.truetype(పథం_జాబితా[0], 13), ImageFont.truetype(పథం_జాబితా[1], 16, index=1), ImageFont.truetype(పథం_జాబితా[2], 16)]
    డేటా = bytearray()
    for అక్షరం_సంకేతీకరణం in list(range(65536)) + list(range(0x1f600, 0x1f650)):
        రేఖాచిత్రణ_మూల్యం = Image.new('L', (16, 16)); 화면그리기 = ImageDraw.Draw(రేఖాచిత్రణ_మూల్యం)
        if not (అక్షరం_సంకేతీకరణం < 32 or 0xd800 <= అక్షరం_సంకేతీకరణం <= 0xdfff):
            화면그리기.text((0, -1 if అక్షరం_సంకేతీకరణం < 256 else -5 if అక్షరం_సంకేతీకరణం < 65536 else -3), chr(అక్షరం_సంకేతీకరణం), font=అక్షరాకృతి_జాబితా[0 if అక్షరం_సంకేతీకరణం < 256 else 1 if అక్షరం_సంకేతీకరణం < 65536 else 2], fill=255)
        for Y_బటన్_సమన్వయపరుచు in range(16):
            నేపథ్యంలో_తెలివైన_బదిలీ_సేవ_జాబితా = 0
            for x_నిర్దేశాంకం in range(16): నేపథ్యంలో_తెలివైన_బదిలీ_సేవ_జాబితా = నేపథ్యంలో_తెలివైన_బదిలీ_సేవ_జాబితా * 2 + (రేఖాచిత్రణ_మూల్యం.getpixel((x_నిర్దేశాంకం, Y_బటన్_సమన్వయపరుచు)) >= 96)
            డేటా += నేపథ్యంలో_తెలివైన_బదిలీ_సేవ_జాబితా.to_bytes(2, 'big')
    లక్ష్యం = ప్రొజెక్ట్_మూలం / 'vendor/terminal-font.bin'; లక్ష్యం.write_bytes(డేటా)
    이용허락목록 = [Path('/usr/share/doc/fonts-noto-cjk/copyright'), Path('/usr/share/doc/fonts-dejavu-core/copyright')]
    for 원본주소 in 이용허락목록: (ప్రొజెక్ట్_మూలం / 'vendor' / ('LICENSE.' + 원본주소.parent.name)).write_bytes(원본주소.read_bytes())
    (ప్రొజెక్ట్_మూలం / 'vendor/terminal-font.json').write_text(json.dumps({'name': 'JKOROS terminal bitmap', 'format': '16 rows, big-endian uint16 mask; BMP then U+1F600..1F64F', 'glyphs': 65536+80, 'sha256': hashlib.sha256(డేటా).hexdigest(), 'sources': {డేటా_స్థాయి: hashlib.sha256(Path(డేటా_స్థాయి).read_bytes()).hexdigest() for డేటా_స్థాయి in పథం_జాబితా}}, indent=2) + '\n')
    print(లక్ష్యం)


if __name__ == '__main__': నడుపుము()
