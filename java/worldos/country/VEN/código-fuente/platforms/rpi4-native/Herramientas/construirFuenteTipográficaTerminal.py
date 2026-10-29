#!/usr/bin/env python3
"""Noto CJK/DejaVu의 라이선스와 출처를 보존한 고정 extensiónRangoAnchura terminal 비트맵 generar. 평상시 빌드는 vendor Archivo valorUsar."""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageDraw, ImageFont
raízProyecto = Path(__file__).resolve().parents[1]


def ponerEnMarcha():
    listaRuta = ['/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']
    listaFuenteTipográfica = [ImageFont.truetype(listaRuta[0], 13), ImageFont.truetype(listaRuta[1], 16, index=1), ImageFont.truetype(listaRuta[2], 16)]
    Datos = bytearray()
    for codificaciónEstadoCarácter in list(range(65536)) + list(range(0x1f600, 0x1f650)):
        Dibujo = Image.new('L', (16, 16)); dibujarPantalla = ImageDraw.Draw(Dibujo)
        if not (codificaciónEstadoCarácter < 32 or 0xd800 <= codificaciónEstadoCarácter <= 0xdfff):
            dibujarPantalla.text((0, -1 if codificaciónEstadoCarácter < 256 else -5 if codificaciónEstadoCarácter < 65536 else -3), chr(codificaciónEstadoCarácter), font=listaFuenteTipográfica[0 if codificaciónEstadoCarácter < 256 else 1 if codificaciónEstadoCarácter < 65536 else 2], fill=255)
        for coordenadaCoordenadaVertical in range(16):
            listaBits = 0
            for coordenadaCoordenadaHorizontal in range(16): listaBits = listaBits * 2 + (Dibujo.getpixel((coordenadaCoordenadaHorizontal, coordenadaCoordenadaVertical)) >= 96)
            Datos += listaBits.to_bytes(2, 'big')
    valorObjetivo = raízProyecto / 'vendor/terminal-font.bin'; valorObjetivo.write_bytes(Datos)
    licencias = [Path('/usr/share/doc/fonts-noto-cjk/copyright'), Path('/usr/share/doc/fonts-dejavu-core/copyright')]
    for direcciónOriginal in licencias: (raízProyecto / 'vendor' / ('LICENSE.' + direcciónOriginal.parent.name)).write_bytes(direcciónOriginal.read_bytes())
    (raízProyecto / 'vendor/terminal-font.json').write_text(json.dumps({'name': 'JKOROS terminal bitmap', 'format': '16 rows, big-endian uint16 mask; BMP then U+1F600..1F64F', 'glyphs': 65536+80, 'sha256': hashlib.sha256(Datos).hexdigest(), 'sources': {posiciónDatos: hashlib.sha256(Path(posiciónDatos).read_bytes()).hexdigest() for posiciónDatos in listaRuta}}, indent=2) + '\n')
    print(valorObjetivo)


if __name__ == '__main__': ponerEnMarcha()
