#!/usr/bin/env python3
"""Noto CJK/DejaVu의 라이선스와 출처를 보존한 고정 폭 terminal 비트맵 gerar. 평상시 빌드는 vendor ficheiro uso_VALOR."""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageDraw, ImageFont
ação_raiz = Path(__file__).resolve().parents[1]


def iniciar():
    caminho_Lista = ['/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']
    fonte_Lista = [ImageFont.truetype(caminho_Lista[0], 13), ImageFont.truetype(caminho_Lista[1], 16, index=1), ImageFont.truetype(caminho_Lista[2], 16)]
    dados = bytearray()
    for codificação_de_caracteres in list(range(65536)) + list(range(0x1f600, 0x1f650)):
        desenho_VALOR = Image.new('L', (16, 16)); emitir_tela = ImageDraw.Draw(desenho_VALOR)
        if not (codificação_de_caracteres < 32 or 0xd800 <= codificação_de_caracteres <= 0xdfff):
            emitir_tela.text((0, -1 if codificação_de_caracteres < 256 else -5 if codificação_de_caracteres < 65536 else -3), chr(codificação_de_caracteres), font=fonte_Lista[0 if codificação_de_caracteres < 256 else 1 if codificação_de_caracteres < 65536 else 2], fill=255)
        for Y_coordenada in range(16):
            BITS_Lista = 0
            for coordenada_X in range(16): BITS_Lista = BITS_Lista * 2 + (desenho_VALOR.getpixel((coordenada_X, Y_coordenada)) >= 96)
            dados += BITS_Lista.to_bytes(2, 'big')
    meta = ação_raiz / 'vendor/terminal-font.bin'; meta.write_bytes(dados)
    이용허락목록 = [Path('/usr/share/doc/fonts-noto-cjk/copyright'), Path('/usr/share/doc/fonts-dejavu-core/copyright')]
    for 원본주소 in 이용허락목록: (ação_raiz / 'vendor' / ('LICENSE.' + 원본주소.parent.name)).write_bytes(원본주소.read_bytes())
    (ação_raiz / 'vendor/terminal-font.json').write_text(json.dumps({'name': 'JKOROS terminal bitmap', 'format': '16 rows, big-endian uint16 mask; BMP then U+1F600..1F64F', 'glyphs': 65536+80, 'sha256': hashlib.sha256(dados).hexdigest(), 'sources': {dados_cargo: hashlib.sha256(Path(dados_cargo).read_bytes()).hexdigest() for dados_cargo in caminho_Lista}}, indent=2) + '\n')
    print(meta)


if __name__ == '__main__': iniciar()
