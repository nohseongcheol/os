#!/usr/bin/env python3
"""Noto CJK/DejaVu의 라이선스와 출처를 보존한 고정 폭 Terminal 비트맵 generar. 평상시 빌드는 vendor Fitxer ús_VALOR."""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageDraw, ImageFont
Project_rel = Path(__file__).resolve().parents[1]


def Executa_2():
    camí_Llista = ['/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']
    tipus_de_lletra_Llista = [ImageFont.truetype(camí_Llista[0], 13), ImageFont.truetype(camí_Llista[1], 16, index=1), ImageFont.truetype(camí_Llista[2], 16)]
    dades = bytearray()
    for caràcter_codificació in list(range(65536)) + list(range(0x1f600, 0x1f650)):
        dibuix_VALOR = Image.new('L', (16, 16)); 화면그리기 = ImageDraw.Draw(dibuix_VALOR)
        if not (caràcter_codificació < 32 or 0xd800 <= caràcter_codificació <= 0xdfff):
            화면그리기.text((0, -1 if caràcter_codificació < 256 else -5 if caràcter_codificació < 65536 else -3), chr(caràcter_codificació), font=tipus_de_lletra_Llista[0 if caràcter_codificació < 256 else 1 if caràcter_codificació < 65536 else 2], fill=255)
        for Y_coordenada in range(16):
            Servei_de_transferència_intel_ligent_en_segon_terme_Llista = 0
            for X_coordenada in range(16): Servei_de_transferència_intel_ligent_en_segon_terme_Llista = Servei_de_transferència_intel_ligent_en_segon_terme_Llista * 2 + (dibuix_VALOR.getpixel((X_coordenada, Y_coordenada)) >= 96)
            dades += Servei_de_transferència_intel_ligent_en_segon_terme_Llista.to_bytes(2, 'big')
    objectiu = Project_rel / 'vendor/terminal-font.bin'; objectiu.write_bytes(dades)
    이용허락목록 = [Path('/usr/share/doc/fonts-noto-cjk/copyright'), Path('/usr/share/doc/fonts-dejavu-core/copyright')]
    for 원본주소 in 이용허락목록: (Project_rel / 'vendor' / ('LICENSE.' + 원본주소.parent.name)).write_bytes(원본주소.read_bytes())
    (Project_rel / 'vendor/terminal-font.json').write_text(json.dumps({'name': 'JKOROS terminal bitmap', 'format': '16 rows, big-endian uint16 mask; BMP then U+1F600..1F64F', 'glyphs': 65536+80, 'sha256': hashlib.sha256(dades).hexdigest(), 'sources': {dades_càrrec: hashlib.sha256(Path(dades_càrrec).read_bytes()).hexdigest() for dades_càrrec in camí_Llista}}, indent=2) + '\n')
    print(objectiu)


if __name__ == '__main__': Executa_2()
