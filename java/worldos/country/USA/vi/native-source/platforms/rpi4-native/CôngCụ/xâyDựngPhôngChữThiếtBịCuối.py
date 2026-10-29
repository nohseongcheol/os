#!/usr/bin/env python3
"""Noto CJK/DejaVu의 라이선스와 출처를 보존한 고정 khoảngTrảiRộng thiếtBịCuối 비트맵 sinh. 평상시 빌드는 vendor Tệp giáTrịDùng."""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageDraw, ImageFont
gốcCâyDựÁn = Path(__file__).resolve().parents[1]


def chạy():
    danhSáchĐườngDẫn = ['/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']
    danhSáchPhôngChữ = [ImageFont.truetype(danhSáchĐườngDẫn[0], 13), ImageFont.truetype(danhSáchĐườngDẫn[1], 16, index=1), ImageFont.truetype(danhSáchĐườngDẫn[2], 16)]
    DữLiệu = bytearray()
    for mãHóaKýTự in list(range(65536)) + list(range(0x1f600, 0x1f650)):
        HìnhVẽ = Image.new('L', (16, 16)); vẽMànHình = ImageDraw.Draw(HìnhVẽ)
        if not (mãHóaKýTự < 32 or 0xd800 <= mãHóaKýTự <= 0xdfff):
            vẽMànHình.text((0, -1 if mãHóaKýTự < 256 else -5 if mãHóaKýTự < 65536 else -3), chr(mãHóaKýTự), font=danhSáchPhôngChữ[0 if mãHóaKýTự < 256 else 1 if mãHóaKýTự < 65536 else 2], fill=255)
        for tọaĐộY in range(16):
            danhSáchCácBit = 0
            for tọaĐộX in range(16): danhSáchCácBit = danhSáchCácBit * 2 + (HìnhVẽ.getpixel((tọaĐộX, tọaĐộY)) >= 96)
            DữLiệu += danhSáchCácBit.to_bytes(2, 'big')
    giáTrịĐốiĐích = gốcCâyDựÁn / 'vendor/terminal-font.bin'; giáTrịĐốiĐích.write_bytes(DữLiệu)
    cácGiấyPhép = [Path('/usr/share/doc/fonts-noto-cjk/copyright'), Path('/usr/share/doc/fonts-dejavu-core/copyright')]
    for địaChỉNguyênBản in cácGiấyPhép: (gốcCâyDựÁn / 'vendor' / ('LICENSE.' + địaChỉNguyênBản.parent.name)).write_bytes(địaChỉNguyênBản.read_bytes())
    (gốcCâyDựÁn / 'vendor/terminal-font.json').write_text(json.dumps({'name': 'JKOROS terminal bitmap', 'format': '16 rows, big-endian uint16 mask; BMP then U+1F600..1F64F', 'glyphs': 65536+80, 'sha256': hashlib.sha256(DữLiệu).hexdigest(), 'sources': {vịTríDữLiệu: hashlib.sha256(Path(vịTríDữLiệu).read_bytes()).hexdigest() for vịTríDữLiệu in danhSáchĐườngDẫn}}, indent=2) + '\n')
    print(giáTrịĐốiĐích)


if __name__ == '__main__': chạy()
