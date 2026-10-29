#!/usr/bin/env python3
"""Noto CJK/DejaVu의 라이선스와 출처를 보존한 고정 폭 Terminal 비트맵 mag_generate. 평상시 빌드는 vendor file 사용."""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageDraw, ImageFont
Project_root = Path(__file__).resolve().parents[1]


def run():
    path_list = ['/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']
    font_list = [ImageFont.truetype(path_list[0], 13), ImageFont.truetype(path_list[1], 16, index=1), ImageFont.truetype(path_list[2], 16)]
    data = bytearray()
    for karakter_pag_encode in list(range(65536)) + list(range(0x1f600, 0x1f650)):
        iginuhit_VALUE = Image.new('L', (16, 16)); 화면그리기 = ImageDraw.Draw(iginuhit_VALUE)
        if not (karakter_pag_encode < 32 or 0xd800 <= karakter_pag_encode <= 0xdfff):
            화면그리기.text((0, -1 if karakter_pag_encode < 256 else -5 if karakter_pag_encode < 65536 else -3), chr(karakter_pag_encode), font=font_list[0 if karakter_pag_encode < 256 else 1 if karakter_pag_encode < 65536 else 2], fill=255)
        for Y_button_coordinate in range(16):
            Background_Intelligent_Transfer_Service_list = 0
            for x_coordinate in range(16): Background_Intelligent_Transfer_Service_list = Background_Intelligent_Transfer_Service_list * 2 + (iginuhit_VALUE.getpixel((x_coordinate, Y_button_coordinate)) >= 96)
            data += Background_Intelligent_Transfer_Service_list.to_bytes(2, 'big')
    layunin = Project_root / 'vendor/terminal-font.bin'; layunin.write_bytes(data)
    이용허락목록 = [Path('/usr/share/doc/fonts-noto-cjk/copyright'), Path('/usr/share/doc/fonts-dejavu-core/copyright')]
    for 원본주소 in 이용허락목록: (Project_root / 'vendor' / ('LICENSE.' + 원본주소.parent.name)).write_bytes(원본주소.read_bytes())
    (Project_root / 'vendor/terminal-font.json').write_text(json.dumps({'name': 'JKOROS terminal bitmap', 'format': '16 rows, big-endian uint16 mask; BMP then U+1F600..1F64F', 'glyphs': 65536+80, 'sha256': hashlib.sha256(data).hexdigest(), 'sources': {data_posisyon: hashlib.sha256(Path(data_posisyon).read_bytes()).hexdigest() for data_posisyon in path_list}}, indent=2) + '\n')
    print(layunin)


if __name__ == '__main__': run()
