#!/usr/bin/env python3
"""Noto CJK/DejaVu의 라이선스와 출처를 보존한 고정 寬度跨度 終端 비트맵 生成. 평상시 빌드는 vendor 檔案 使用值."""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageDraw, ImageFont
項目根 = Path(__file__).resolve().parents[1]


def 運行():
    路徑列表 = ['/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']
    字體列表 = [ImageFont.truetype(路徑列表[0], 13), ImageFont.truetype(路徑列表[1], 16, index=1), ImageFont.truetype(路徑列表[2], 16)]
    資料 = bytearray()
    for 字元編碼狀態 in list(range(65536)) + list(range(0x1f600, 0x1f650)):
        繪圖 = Image.new('L', (16, 16)); 繪製屏幕 = ImageDraw.Draw(繪圖)
        if not (字元編碼狀態 < 32 or 0xd800 <= 字元編碼狀態 <= 0xdfff):
            繪製屏幕.text((0, -1 if 字元編碼狀態 < 256 else -5 if 字元編碼狀態 < 65536 else -3), chr(字元編碼狀態), font=字體列表[0 if 字元編碼狀態 < 256 else 1 if 字元編碼狀態 < 65536 else 2], fill=255)
        for Y_按鈕座標 in range(16):
            位元列列表 = 0
            for 橫座標座標 in range(16): 位元列列表 = 位元列列表 * 2 + (繪圖.getpixel((橫座標座標, Y_按鈕座標)) >= 96)
            資料 += 位元列列表.to_bytes(2, 'big')
    目標值 = 項目根 / 'vendor/terminal-font.bin'; 目標值.write_bytes(資料)
    許可列 = [Path('/usr/share/doc/fonts-noto-cjk/copyright'), Path('/usr/share/doc/fonts-dejavu-core/copyright')]
    for 原始地址 in 許可列: (項目根 / 'vendor' / ('LICENSE.' + 原始地址.parent.name)).write_bytes(原始地址.read_bytes())
    (項目根 / 'vendor/terminal-font.json').write_text(json.dumps({'name': 'JKOROS terminal bitmap', 'format': '16 rows, big-endian uint16 mask; BMP then U+1F600..1F64F', 'glyphs': 65536+80, 'sha256': hashlib.sha256(資料).hexdigest(), 'sources': {資料位置: hashlib.sha256(Path(資料位置).read_bytes()).hexdigest() for 資料位置 in 路徑列表}}, indent=2) + '\n')
    print(目標值)


if __name__ == '__main__': 運行()
