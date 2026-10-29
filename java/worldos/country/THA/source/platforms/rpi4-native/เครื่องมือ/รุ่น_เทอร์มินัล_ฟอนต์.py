#!/usr/bin/env python3
"""Noto CJK/DejaVu의 라이선스와 출처를 보존한 고정 폭 เทอร์มินัล 비트맵 สร้าง_167eff27. 평상시 빌드는 vendor แฟ้ม ใช้_ค่า."""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageDraw, ImageFont
แสดง_ราก = Path(__file__).resolve().parents[1]


def เรียกใช้งาน():
    พาธ_รายการ = ['/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']
    ฟอนต์_รายการ = [ImageFont.truetype(พาธ_รายการ[0], 13), ImageFont.truetype(พาธ_รายการ[1], 16, index=1), ImageFont.truetype(พาธ_รายการ[2], 16)]
    ข้อมูล = bytearray()
    for อักขระ_การเข้ารหัส in list(range(65536)) + list(range(0x1f600, 0x1f650)):
        รูปวาด_ค่า = Image.new('L', (16, 16)); 화면그리기 = ImageDraw.Draw(รูปวาด_ค่า)
        if not (อักขระ_การเข้ารหัส < 32 or 0xd800 <= อักขระ_การเข้ารหัส <= 0xdfff):
            화면그리기.text((0, -1 if อักขระ_การเข้ารหัส < 256 else -5 if อักขระ_การเข้ารหัส < 65536 else -3), chr(อักขระ_การเข้ารหัส), font=ฟอนต์_รายการ[0 if อักขระ_การเข้ารหัส < 256 else 1 if อักขระ_การเข้ารหัส < 65536 else 2], fill=255)
        for 세로좌표 in range(16):
            비트들 = 0
            for พิกัดแกน_x in range(16): 비트들 = 비트들 * 2 + (รูปวาด_ค่า.getpixel((พิกัดแกน_x, 세로좌표)) >= 96)
            ข้อมูล += 비트들.to_bytes(2, 'big')
    เป้าหมาย = แสดง_ราก / 'vendor/terminal-font.bin'; เป้าหมาย.write_bytes(ข้อมูล)
    이용허락목록 = [Path('/usr/share/doc/fonts-noto-cjk/copyright'), Path('/usr/share/doc/fonts-dejavu-core/copyright')]
    for 원본주소 in 이용허락목록: (แสดง_ราก / 'vendor' / ('LICENSE.' + 원본주소.parent.name)).write_bytes(원본주소.read_bytes())
    (แสดง_ราก / 'vendor/terminal-font.json').write_text(json.dumps({'name': 'JKOROS terminal bitmap', 'format': '16 rows, big-endian uint16 mask; BMP then U+1F600..1F64F', 'glyphs': 65536+80, 'sha256': hashlib.sha256(ข้อมูล).hexdigest(), 'sources': {ข้อมูล_ตําแหน่ง: hashlib.sha256(Path(ข้อมูล_ตําแหน่ง).read_bytes()).hexdigest() for ข้อมูล_ตําแหน่ง in พาธ_รายการ}}, indent=2) + '\n')
    print(เป้าหมาย)


if __name__ == '__main__': เรียกใช้งาน()
