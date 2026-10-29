#!/usr/bin/env python3
"""Noto CJK/DejaVu의 라이선스와 출처를 보존한 고정 폭 terminale 비트맵 generare. 평상시 빌드는 vendor file usare_VALORE."""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageDraw, ImageFont
azione_radice = Path(__file__).resolve().parents[1]


def avvia():
    percorso_elenco = ['/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']
    tipo_di_carattere_elenco = [ImageFont.truetype(percorso_elenco[0], 13), ImageFont.truetype(percorso_elenco[1], 16, index=1), ImageFont.truetype(percorso_elenco[2], 16)]
    dati = bytearray()
    for codifica_dei_caratteri in list(range(65536)) + list(range(0x1f600, 0x1f650)):
        disegno_VALORE = Image.new('L', (16, 16)); Disegno_schermata = ImageDraw.Draw(disegno_VALORE)
        if not (codifica_dei_caratteri < 32 or 0xd800 <= codifica_dei_caratteri <= 0xdfff):
            Disegno_schermata.text((0, -1 if codifica_dei_caratteri < 256 else -5 if codifica_dei_caratteri < 65536 else -3), chr(codifica_dei_caratteri), font=tipo_di_carattere_elenco[0 if codifica_dei_caratteri < 256 else 1 if codifica_dei_caratteri < 65536 else 2], fill=255)
        for Y_coordinata in range(16):
            BITS_elenco = 0
            for coordinata_x in range(16): BITS_elenco = BITS_elenco * 2 + (disegno_VALORE.getpixel((coordinata_x, Y_coordinata)) >= 96)
            dati += BITS_elenco.to_bytes(2, 'big')
    target = azione_radice / 'vendor/terminal-font.bin'; target.write_bytes(dati)
    이용허락목록 = [Path('/usr/share/doc/fonts-noto-cjk/copyright'), Path('/usr/share/doc/fonts-dejavu-core/copyright')]
    for 원본주소 in 이용허락목록: (azione_radice / 'vendor' / ('LICENSE.' + 원본주소.parent.name)).write_bytes(원본주소.read_bytes())
    (azione_radice / 'vendor/terminal-font.json').write_text(json.dumps({'name': 'JKOROS terminal bitmap', 'format': '16 rows, big-endian uint16 mask; BMP then U+1F600..1F64F', 'glyphs': 65536+80, 'sha256': hashlib.sha256(dati).hexdigest(), 'sources': {dati_funzione: hashlib.sha256(Path(dati_funzione).read_bytes()).hexdigest() for dati_funzione in percorso_elenco}}, indent=2) + '\n')
    print(target)


if __name__ == '__main__': avvia()
