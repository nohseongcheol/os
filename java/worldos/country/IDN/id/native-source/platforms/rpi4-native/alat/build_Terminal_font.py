#!/usr/bin/env python3
"""Noto CJK/DejaVu의 라이선스와 출처를 보존한 고정 폭 terminal 비트맵 buat. 평상시 빌드는 vendor berkas gunakan_VALUE."""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageDraw, ImageFont
Tugas_akar = Path(__file__).resolve().parents[1]


def jalankan():
    jalur_Daftar = ['/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']
    font_Daftar = [ImageFont.truetype(jalur_Daftar[0], 13), ImageFont.truetype(jalur_Daftar[1], 16, index=1), ImageFont.truetype(jalur_Daftar[2], 16)]
    data = bytearray()
    for pengodean_karakter in list(range(65536)) + list(range(0x1f600, 0x1f650)):
        gambar_VALUE = Image.new('L', (16, 16)); 화면그리기 = ImageDraw.Draw(gambar_VALUE)
        if not (pengodean_karakter < 32 or 0xd800 <= pengodean_karakter <= 0xdfff):
            화면그리기.text((0, -1 if pengodean_karakter < 256 else -5 if pengodean_karakter < 65536 else -3), chr(pengodean_karakter), font=font_Daftar[0 if pengodean_karakter < 256 else 1 if pengodean_karakter < 65536 else 2], fill=255)
        for Y_koordinat in range(16):
            Background_Intelligent_Transfer_Service_Daftar = 0
            for koordinat_x in range(16): Background_Intelligent_Transfer_Service_Daftar = Background_Intelligent_Transfer_Service_Daftar * 2 + (gambar_VALUE.getpixel((koordinat_x, Y_koordinat)) >= 96)
            data += Background_Intelligent_Transfer_Service_Daftar.to_bytes(2, 'big')
    target = Tugas_akar / 'vendor/terminal-font.bin'; target.write_bytes(data)
    이용허락목록 = [Path('/usr/share/doc/fonts-noto-cjk/copyright'), Path('/usr/share/doc/fonts-dejavu-core/copyright')]
    for 원본주소 in 이용허락목록: (Tugas_akar / 'vendor' / ('LICENSE.' + 원본주소.parent.name)).write_bytes(원본주소.read_bytes())
    (Tugas_akar / 'vendor/terminal-font.json').write_text(json.dumps({'name': 'JKOROS terminal bitmap', 'format': '16 rows, big-endian uint16 mask; BMP then U+1F600..1F64F', 'glyphs': 65536+80, 'sha256': hashlib.sha256(data).hexdigest(), 'sources': {data_posisi: hashlib.sha256(Path(data_posisi).read_bytes()).hexdigest() for data_posisi in jalur_Daftar}}, indent=2) + '\n')
    print(target)


if __name__ == '__main__': jalankan()
