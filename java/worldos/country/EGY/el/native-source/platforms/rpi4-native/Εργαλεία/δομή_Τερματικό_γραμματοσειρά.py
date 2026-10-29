#!/usr/bin/env python3
"""Noto CJK/DejaVu의 라이선스와 출처를 보존한 고정 폭 Τερματικό 비트맵 δημιουργώ. 평상시 빌드는 vendor Αρχείο χρήση_τιμή."""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageDraw, ImageFont
έργο_ρίζα = Path(__file__).resolve().parents[1]


def Εκτέλεση_2():
    διαδρομή_Λίστα = ['/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']
    γραμματοσειρά_Λίστα = [ImageFont.truetype(διαδρομή_Λίστα[0], 13), ImageFont.truetype(διαδρομή_Λίστα[1], 16, index=1), ImageFont.truetype(διαδρομή_Λίστα[2], 16)]
    δεδομένα = bytearray()
    for κωδικοποίηση_χαρακτήρα in list(range(65536)) + list(range(0x1f600, 0x1f650)):
        σχέδιο_τιμή = Image.new('L', (16, 16)); 화면그리기 = ImageDraw.Draw(σχέδιο_τιμή)
        if not (κωδικοποίηση_χαρακτήρα < 32 or 0xd800 <= κωδικοποίηση_χαρακτήρα <= 0xdfff):
            화면그리기.text((0, -1 if κωδικοποίηση_χαρακτήρα < 256 else -5 if κωδικοποίηση_χαρακτήρα < 65536 else -3), chr(κωδικοποίηση_χαρακτήρα), font=γραμματοσειρά_Λίστα[0 if κωδικοποίηση_χαρακτήρα < 256 else 1 if κωδικοποίηση_χαρακτήρα < 65536 else 2], fill=255)
        for κουμπί_Y_συντονισμός in range(16):
            Υπηρεσία_έξυπνης_μεταφοράς_στο_παρασκήνιο_Λίστα = 0
            for συντεταγμένη_x in range(16): Υπηρεσία_έξυπνης_μεταφοράς_στο_παρασκήνιο_Λίστα = Υπηρεσία_έξυπνης_μεταφοράς_στο_παρασκήνιο_Λίστα * 2 + (σχέδιο_τιμή.getpixel((συντεταγμένη_x, κουμπί_Y_συντονισμός)) >= 96)
            δεδομένα += Υπηρεσία_έξυπνης_μεταφοράς_στο_παρασκήνιο_Λίστα.to_bytes(2, 'big')
    τιμή_στόχος = έργο_ρίζα / 'vendor/terminal-font.bin'; τιμή_στόχος.write_bytes(δεδομένα)
    이용허락목록 = [Path('/usr/share/doc/fonts-noto-cjk/copyright'), Path('/usr/share/doc/fonts-dejavu-core/copyright')]
    for 원본주소 in 이용허락목록: (έργο_ρίζα / 'vendor' / ('LICENSE.' + 원본주소.parent.name)).write_bytes(원본주소.read_bytes())
    (έργο_ρίζα / 'vendor/terminal-font.json').write_text(json.dumps({'name': 'JKOROS terminal bitmap', 'format': '16 rows, big-endian uint16 mask; BMP then U+1F600..1F64F', 'glyphs': 65536+80, 'sha256': hashlib.sha256(δεδομένα).hexdigest(), 'sources': {δεδομένα_θέση: hashlib.sha256(Path(δεδομένα_θέση).read_bytes()).hexdigest() for δεδομένα_θέση in διαδρομή_Λίστα}}, indent=2) + '\n')
    print(τιμή_στόχος)


if __name__ == '__main__': Εκτέλεση_2()
