#!/usr/bin/env python3
"""Noto CJK/DejaVu의 라이선스와 출처를 보존한 고정 폭 Terminal 비트맵 yarat. 평상시 빌드는 vendor FAYL 사용."""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageDraw, ImageFont
Project_kök = Path(__file__).resolve().parents[1]


def İcra_Et():
    yol_Siyahı = ['/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']
    şrift_Siyahı = [ImageFont.truetype(yol_Siyahı[0], 13), ImageFont.truetype(yol_Siyahı[1], 16, index=1), ImageFont.truetype(yol_Siyahı[2], 16)]
    verilənlər = bytearray()
    for simvol_kodlaşdırma in list(range(65536)) + list(range(0x1f600, 0x1f650)):
        rəsm_VALUE = Image.new('L', (16, 16)); 화면그리기 = ImageDraw.Draw(rəsm_VALUE)
        if not (simvol_kodlaşdırma < 32 or 0xd800 <= simvol_kodlaşdırma <= 0xdfff):
            화면그리기.text((0, -1 if simvol_kodlaşdırma < 256 else -5 if simvol_kodlaşdırma < 65536 else -3), chr(simvol_kodlaşdırma), font=şrift_Siyahı[0 if simvol_kodlaşdırma < 256 else 1 if simvol_kodlaşdırma < 65536 else 2], fill=255)
        for Y_koordinat in range(16):
            Fon_Ağıllı_Ötürmə_Xidməti_Siyahı = 0
            for x_koordinatı in range(16): Fon_Ağıllı_Ötürmə_Xidməti_Siyahı = Fon_Ağıllı_Ötürmə_Xidməti_Siyahı * 2 + (rəsm_VALUE.getpixel((x_koordinatı, Y_koordinat)) >= 96)
            verilənlər += Fon_Ağıllı_Ötürmə_Xidməti_Siyahı.to_bytes(2, 'big')
    hədəf = Project_kök / 'vendor/terminal-font.bin'; hədəf.write_bytes(verilənlər)
    이용허락목록 = [Path('/usr/share/doc/fonts-noto-cjk/copyright'), Path('/usr/share/doc/fonts-dejavu-core/copyright')]
    for 원본주소 in 이용허락목록: (Project_kök / 'vendor' / ('LICENSE.' + 원본주소.parent.name)).write_bytes(원본주소.read_bytes())
    (Project_kök / 'vendor/terminal-font.json').write_text(json.dumps({'name': 'JKOROS terminal bitmap', 'format': '16 rows, big-endian uint16 mask; BMP then U+1F600..1F64F', 'glyphs': 65536+80, 'sha256': hashlib.sha256(verilənlər).hexdigest(), 'sources': {verilənlər_yerinə_qoymaq: hashlib.sha256(Path(verilənlər_yerinə_qoymaq).read_bytes()).hexdigest() for verilənlər_yerinə_qoymaq in yol_Siyahı}}, indent=2) + '\n')
    print(hədəf)


if __name__ == '__main__': İcra_Et()
