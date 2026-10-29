#!/usr/bin/env python3
"""Noto CJK/DejaVu의 라이선스와 출처를 보존한 고정 幅跨域 端末 비트맵 生成. 평상시 빌드는 vendor ファイル 使用値."""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageDraw, ImageFont
計画根 = Path(__file__).resolve().parents[1]


def 起動処理():
    経路一覧 = ['/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']
    書体一覧 = [ImageFont.truetype(経路一覧[0], 13), ImageFont.truetype(経路一覧[1], 16, index=1), ImageFont.truetype(経路一覧[2], 16)]
    データ = bytearray()
    for 文字符号化状態 in list(range(65536)) + list(range(0x1f600, 0x1f650)):
        描画 = Image.new('L', (16, 16)); 画面描画処理 = ImageDraw.Draw(描画)
        if not (文字符号化状態 < 32 or 0xd800 <= 文字符号化状態 <= 0xdfff):
            画面描画処理.text((0, -1 if 文字符号化状態 < 256 else -5 if 文字符号化状態 < 65536 else -3), chr(文字符号化状態), font=書体一覧[0 if 文字符号化状態 < 256 else 1 if 文字符号化状態 < 65536 else 2], fill=255)
        for 縦座標 in range(16):
            ビット列一覧 = 0
            for 横座標 in range(16): ビット列一覧 = ビット列一覧 * 2 + (描画.getpixel((横座標, 縦座標)) >= 96)
            データ += ビット列一覧.to_bytes(2, 'big')
    対象値 = 計画根 / 'vendor/terminal-font.bin'; 対象値.write_bytes(データ)
    利用許諾一覧 = [Path('/usr/share/doc/fonts-noto-cjk/copyright'), Path('/usr/share/doc/fonts-dejavu-core/copyright')]
    for 原本番地 in 利用許諾一覧: (計画根 / 'vendor' / ('LICENSE.' + 原本番地.parent.name)).write_bytes(原本番地.read_bytes())
    (計画根 / 'vendor/terminal-font.json').write_text(json.dumps({'name': 'JKOROS terminal bitmap', 'format': '16 rows, big-endian uint16 mask; BMP then U+1F600..1F64F', 'glyphs': 65536+80, 'sha256': hashlib.sha256(データ).hexdigest(), 'sources': {データ位置: hashlib.sha256(Path(データ位置).read_bytes()).hexdigest() for データ位置 in 経路一覧}}, indent=2) + '\n')
    print(対象値)


if __name__ == '__main__': 起動処理()
