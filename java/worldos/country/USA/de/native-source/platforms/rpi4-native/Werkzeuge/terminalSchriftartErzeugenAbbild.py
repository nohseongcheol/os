#!/usr/bin/env python3
"""Noto CJK/DejaVu의 라이선스와 출처를 보존한 고정 breiteSpannweite terminal 비트맵 generieren. 평상시 빌드는 vendor Datei benutzenWert."""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageDraw, ImageFont
projektWurzel = Path(__file__).resolve().parents[1]


def ausführenVorgang():
    pfadListe = ['/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']
    schriftartListe = [ImageFont.truetype(pfadListe[0], 13), ImageFont.truetype(pfadListe[1], 16, index=1), ImageFont.truetype(pfadListe[2], 16)]
    Daten = bytearray()
    for zeichenKodierung in list(range(65536)) + list(range(0x1f600, 0x1f650)):
        Zeichnung = Image.new('L', (16, 16)); bildschirmZeichnen = ImageDraw.Draw(Zeichnung)
        if not (zeichenKodierung < 32 or 0xd800 <= zeichenKodierung <= 0xdfff):
            bildschirmZeichnen.text((0, -1 if zeichenKodierung < 256 else -5 if zeichenKodierung < 65536 else -3), chr(zeichenKodierung), font=schriftartListe[0 if zeichenKodierung < 256 else 1 if zeichenKodierung < 65536 else 2], fill=255)
        for senkrechteKoordinateKoordinate in range(16):
            bitlisteListe = 0
            for waagerechteKoordinateKoordinate in range(16): bitlisteListe = bitlisteListe * 2 + (Zeichnung.getpixel((waagerechteKoordinateKoordinate, senkrechteKoordinateKoordinate)) >= 96)
            Daten += bitlisteListe.to_bytes(2, 'big')
    zielobjektWert = projektWurzel / 'vendor/terminal-font.bin'; zielobjektWert.write_bytes(Daten)
    lizenzen = [Path('/usr/share/doc/fonts-noto-cjk/copyright'), Path('/usr/share/doc/fonts-dejavu-core/copyright')]
    for ursprünglichAdresse in lizenzen: (projektWurzel / 'vendor' / ('LICENSE.' + ursprünglichAdresse.parent.name)).write_bytes(ursprünglichAdresse.read_bytes())
    (projektWurzel / 'vendor/terminal-font.json').write_text(json.dumps({'name': 'JKOROS terminal bitmap', 'format': '16 rows, big-endian uint16 mask; BMP then U+1F600..1F64F', 'glyphs': 65536+80, 'sha256': hashlib.sha256(Daten).hexdigest(), 'sources': {datenPosition: hashlib.sha256(Path(datenPosition).read_bytes()).hexdigest() for datenPosition in pfadListe}}, indent=2) + '\n')
    print(zielobjektWert)


if __name__ == '__main__': ausführenVorgang()
