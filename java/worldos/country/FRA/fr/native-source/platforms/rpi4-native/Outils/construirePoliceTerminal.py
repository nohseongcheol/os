#!/usr/bin/env python3
"""Noto CJK/DejaVu의 라이선스와 출처를 보존한 고정 étendueLargeur terminal 비트맵 générer. 평상시 빌드는 vendor Fichier valeurUtiliser."""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageDraw, ImageFont
racineProjet = Path(__file__).resolve().parents[1]


def lancer():
    listeChemin = ['/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']
    listePolice = [ImageFont.truetype(listeChemin[0], 13), ImageFont.truetype(listeChemin[1], 16, index=1), ImageFont.truetype(listeChemin[2], 16)]
    Données = bytearray()
    for encodageCaractère in list(range(65536)) + list(range(0x1f600, 0x1f650)):
        Dessin = Image.new('L', (16, 16)); dessinerÉcran = ImageDraw.Draw(Dessin)
        if not (encodageCaractère < 32 or 0xd800 <= encodageCaractère <= 0xdfff):
            dessinerÉcran.text((0, -1 if encodageCaractère < 256 else -5 if encodageCaractère < 65536 else -3), chr(encodageCaractère), font=listePolice[0 if encodageCaractère < 256 else 1 if encodageCaractère < 65536 else 2], fill=255)
        for coordonnéeCoordonnéeVerticale in range(16):
            listeBits = 0
            for coordonnéeCoordonnéeHorizontale in range(16): listeBits = listeBits * 2 + (Dessin.getpixel((coordonnéeCoordonnéeHorizontale, coordonnéeCoordonnéeVerticale)) >= 96)
            Données += listeBits.to_bytes(2, 'big')
    valeurCible = racineProjet / 'vendor/terminal-font.bin'; valeurCible.write_bytes(Données)
    licences = [Path('/usr/share/doc/fonts-noto-cjk/copyright'), Path('/usr/share/doc/fonts-dejavu-core/copyright')]
    for adresseOriginal in licences: (racineProjet / 'vendor' / ('LICENSE.' + adresseOriginal.parent.name)).write_bytes(adresseOriginal.read_bytes())
    (racineProjet / 'vendor/terminal-font.json').write_text(json.dumps({'name': 'JKOROS terminal bitmap', 'format': '16 rows, big-endian uint16 mask; BMP then U+1F600..1F64F', 'glyphs': 65536+80, 'sha256': hashlib.sha256(Données).hexdigest(), 'sources': {positionDonnées: hashlib.sha256(Path(positionDonnées).read_bytes()).hexdigest() for positionDonnées in listeChemin}}, indent=2) + '\n')
    print(valeurCible)


if __name__ == '__main__': lancer()
