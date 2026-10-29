#!/usr/bin/env python3
"""Noto CJK/DejaVu의 라이선스와 출처를 보존한 고정 宽度跨度 终端 비트맵 生成. 평상시 빌드는 vendor 文件 使用值."""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageDraw, ImageFont
项目根 = Path(__file__).resolve().parents[1]


def 运行():
    路径列表 = ['/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']
    字体列表 = [ImageFont.truetype(路径列表[0], 13), ImageFont.truetype(路径列表[1], 16, index=1), ImageFont.truetype(路径列表[2], 16)]
    数据 = bytearray()
    for 字符编码状态 in list(range(65536)) + list(range(0x1f600, 0x1f650)):
        绘图 = Image.new('L', (16, 16)); 绘制屏幕 = ImageDraw.Draw(绘图)
        if not (字符编码状态 < 32 or 0xd800 <= 字符编码状态 <= 0xdfff):
            绘制屏幕.text((0, -1 if 字符编码状态 < 256 else -5 if 字符编码状态 < 65536 else -3), chr(字符编码状态), font=字体列表[0 if 字符编码状态 < 256 else 1 if 字符编码状态 < 65536 else 2], fill=255)
        for Y_按钮坐标 in range(16):
            位列列表 = 0
            for 横坐标坐标 in range(16): 位列列表 = 位列列表 * 2 + (绘图.getpixel((横坐标坐标, Y_按钮坐标)) >= 96)
            数据 += 位列列表.to_bytes(2, 'big')
    目标值 = 项目根 / 'vendor/terminal-font.bin'; 目标值.write_bytes(数据)
    许可列 = [Path('/usr/share/doc/fonts-noto-cjk/copyright'), Path('/usr/share/doc/fonts-dejavu-core/copyright')]
    for 原始地址 in 许可列: (项目根 / 'vendor' / ('LICENSE.' + 原始地址.parent.name)).write_bytes(原始地址.read_bytes())
    (项目根 / 'vendor/terminal-font.json').write_text(json.dumps({'name': 'JKOROS terminal bitmap', 'format': '16 rows, big-endian uint16 mask; BMP then U+1F600..1F64F', 'glyphs': 65536+80, 'sha256': hashlib.sha256(数据).hexdigest(), 'sources': {数据位置: hashlib.sha256(Path(数据位置).read_bytes()).hexdigest() for 数据位置 in 路径列表}}, indent=2) + '\n')
    print(目标值)


if __name__ == '__main__': 运行()
