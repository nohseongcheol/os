#!/usr/bin/env python3
"""Noto CJK/DejaVu의 라이선스와 출처를 보존한 고정 폭 Terminalas 비트맵 generuoti. 평상시 빌드는 vendor Failas naudoti_VALUE."""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageDraw, ImageFont
Project_šaknis = Path(__file__).resolve().parents[1]


def Paleisti():
    kelias_Sąrašas = ['/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']
    šriftas_Sąrašas = [ImageFont.truetype(kelias_Sąrašas[0], 13), ImageFont.truetype(kelias_Sąrašas[1], 16, index=1), ImageFont.truetype(kelias_Sąrašas[2], 16)]
    duomenys = bytearray()
    for simbolių_koduotė in list(range(65536)) + list(range(0x1f600, 0x1f650)):
        piešinys_VALUE = Image.new('L', (16, 16)); 화면그리기 = ImageDraw.Draw(piešinys_VALUE)
        if not (simbolių_koduotė < 32 or 0xd800 <= simbolių_koduotė <= 0xdfff):
            화면그리기.text((0, -1 if simbolių_koduotė < 256 else -5 if simbolių_koduotė < 65536 else -3), chr(simbolių_koduotė), font=šriftas_Sąrašas[0 if simbolių_koduotė < 256 else 1 if simbolių_koduotė < 65536 else 2], fill=255)
        for 세로좌표 in range(16):
            foninio_intelektualiojo_perdavimo_tarnyba_Sąrašas = 0
            for x_koordinatė in range(16): foninio_intelektualiojo_perdavimo_tarnyba_Sąrašas = foninio_intelektualiojo_perdavimo_tarnyba_Sąrašas * 2 + (piešinys_VALUE.getpixel((x_koordinatė, 세로좌표)) >= 96)
            duomenys += foninio_intelektualiojo_perdavimo_tarnyba_Sąrašas.to_bytes(2, 'big')
    tikslas = Project_šaknis / 'vendor/terminal-font.bin'; tikslas.write_bytes(duomenys)
    이용허락목록 = [Path('/usr/share/doc/fonts-noto-cjk/copyright'), Path('/usr/share/doc/fonts-dejavu-core/copyright')]
    for 원본주소 in 이용허락목록: (Project_šaknis / 'vendor' / ('LICENSE.' + 원본주소.parent.name)).write_bytes(원본주소.read_bytes())
    (Project_šaknis / 'vendor/terminal-font.json').write_text(json.dumps({'name': 'JKOROS terminal bitmap', 'format': '16 rows, big-endian uint16 mask; BMP then U+1F600..1F64F', 'glyphs': 65536+80, 'sha256': hashlib.sha256(duomenys).hexdigest(), 'sources': {duomenys_padėtis: hashlib.sha256(Path(duomenys_padėtis).read_bytes()).hexdigest() for duomenys_padėtis in kelias_Sąrašas}}, indent=2) + '\n')
    print(tikslas)


if __name__ == '__main__': Paleisti()
