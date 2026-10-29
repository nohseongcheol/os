#!/usr/bin/env python3
"""Noto CJK/DejaVu의 라이선스와 출처를 보존한 고정 폭 Terminal 비트맵 xerar. 평상시 빌드는 vendor Ficheiro 사용."""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageDraw, ImageFont
Project_raíz = Path(__file__).resolve().parents[1]


def Executar_2():
    camiño_Lista = ['/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']
    tipo_de_letra_Lista = [ImageFont.truetype(camiño_Lista[0], 13), ImageFont.truetype(camiño_Lista[1], 16, index=1), ImageFont.truetype(camiño_Lista[2], 16)]
    datos = bytearray()
    for carácter_codificación in list(range(65536)) + list(range(0x1f600, 0x1f650)):
        그림 = Image.new('L', (16, 16)); 화면그리기 = ImageDraw.Draw(그림)
        if not (carácter_codificación < 32 or 0xd800 <= carácter_codificación <= 0xdfff):
            화면그리기.text((0, -1 if carácter_codificación < 256 else -5 if carácter_codificación < 65536 else -3), chr(carácter_codificación), font=tipo_de_letra_Lista[0 if carácter_codificación < 256 else 1 if carácter_codificación < 65536 else 2], fill=255)
        for Y_coordenada in range(16):
            Servizo_de_transferencia_intelixente_en_segundo_plano_Lista = 0
            for X_coordenada in range(16): Servizo_de_transferencia_intelixente_en_segundo_plano_Lista = Servizo_de_transferencia_intelixente_en_segundo_plano_Lista * 2 + (그림.getpixel((X_coordenada, Y_coordenada)) >= 96)
            datos += Servizo_de_transferencia_intelixente_en_segundo_plano_Lista.to_bytes(2, 'big')
    obxectivo_VALOR = Project_raíz / 'vendor/terminal-font.bin'; obxectivo_VALOR.write_bytes(datos)
    이용허락목록 = [Path('/usr/share/doc/fonts-noto-cjk/copyright'), Path('/usr/share/doc/fonts-dejavu-core/copyright')]
    for 원본주소 in 이용허락목록: (Project_raíz / 'vendor' / ('LICENSE.' + 원본주소.parent.name)).write_bytes(원본주소.read_bytes())
    (Project_raíz / 'vendor/terminal-font.json').write_text(json.dumps({'name': 'JKOROS terminal bitmap', 'format': '16 rows, big-endian uint16 mask; BMP then U+1F600..1F64F', 'glyphs': 65536+80, 'sha256': hashlib.sha256(datos).hexdigest(), 'sources': {datos_cargo: hashlib.sha256(Path(datos_cargo).read_bytes()).hexdigest() for datos_cargo in camiño_Lista}}, indent=2) + '\n')
    print(obxectivo_VALOR)


if __name__ == '__main__': Executar_2()
